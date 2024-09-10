from flask import Blueprint, redirect, render_template, request, session

from flask_session import Session

from ..helpers.helpers import (admin_required, apology, get_stock,
                               login_required)
from .application import Application

#instanciando blueprint
bp = Blueprint('main', __name__)


@bp.route('/admin/register', methods=["POST", "GET"])
def admin_register():
    if request.method == 'GET':
        adm = True
        return render_template('register.html', adm=adm)
    app = Application()
    username = request.form.get('username')
    password = request.form.get('pwd')
    admin = 1
    app.register_user(username, password, admin)
    return redirect('/login')


@bp.route('/admin', methods=["GET", "POST"])
@admin_required
def admin_index():
    app = Application()
    
    users = app.get_users()
    wallets = app.get_wallets()
    records = app.get_records()

    return render_template("admin.html", users=users, wallets=wallets, records=records)


@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('pwd')

    app = Application()
    user = app.get_user(username, password)
    if not app.authenticate_user(username, password):
        return apology('Usuário não encontrado')
    
    session['user_id'] = user[0]
    session['role'] = user[3]

    return redirect('/')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    app = Application()
    username = request.form.get('username')
    password = request.form.get('pwd')
    app.register_user(username, password)
    return redirect('/login')


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    app = Application()

    wallet = app.db.get_wallet(session['user_id'])
    return render_template('index.html', wallet=wallet)

# comprar stocks
@bp.route("/buy", methods=['GET', 'POST'])
@bp.route("/buy/<string:symbol>/<float:price>", methods=['GET', 'POST'])
@login_required
def buy(symbol=None, price=None):
    if request.method == 'GET':
        return render_template('buy.html')
    app = Application()
    if symbol is None:
        symbol = request.form.get('stock')
        price = get_stock(symbol)['price']
        if get_stock(symbol) is not None:
            length = len(symbol)
            return render_template('buy.html', symbol=symbol, price=price, length=length)
        return apology('Ação não encontrada', 404)
    qtd = float(request.form.get('qtd'))
    app.buy_stock(symbol, qtd, price, session["user_id"])
    return redirect('/')
    

# vender stocks
@bp.route("/sell", methods= ["GET", "POST"])
@bp.route("/sell/<string:symbol>/<float:price>", methods= ["GET", "POST"])
@login_required
def sell(symbol=None, price=None):
    if request.method == "GET":
        return render_template("sell.html")
    
    app = Application()

    if symbol is None:
        symbol = request.form.get('stock').upper()
        price = get_stock(symbol)['price']
        if app.search_stock(symbol, session['user_id']):
            length = len(symbol)
            return render_template("sell.html", symbol=symbol, price=price, length=length)
        return apology("Operação inválida!")
    
    qtd = float(request.form.get('qtd'))
    if app.sell_stock(symbol, qtd, price, session["user_id"]) is False:
        return apology("Operação inválida!")
    return redirect("/")

# deletar stock
@bp.route("/stock/<int:user_id>/<string:stock>/delete", methods=["GET", "POST"])
def delete_stock(user_id, stock):
    app = Application()
    app.delete_stock(stock, user_id)
    return redirect('/admin')

# visualizar stock
@bp.route("/stock/<int:user_id>/<string:stock>", methods=["GET", "POST"])
def stock(user_id, stock):
    app = Application()
    stock = app.get_stock(stock, user_id)
    return render_template('stock.html', stock=stock)

# editar stock
@bp.route("/stock/<int:user_id>/<string:stock>/edit", methods=["GET", "POST"])
def edit_stock(user_id, stock):
    app = Application()
    qtd = request.form.get('qtd')
    price = request.form.get('price')
    app.edit_stock(stock, qtd, price, user_id)
    return redirect('/stock/{}/{}'.format(user_id, stock))


# deletar histórico
@bp.route("/records/<int:order_id>/delete", methods=["GET", "POST"])
def delete_records(order_id):
    app = Application()
    app.delete_record(order_id)
    return redirect('/admin')


# historico
@bp.route("/records")
def records():
    app = Application()
    history = app.db.get_records(session['user_id'])
    return render_template('records.html', history=history)



@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@bp.route('/user/<int:id>', methods=['GET', 'POST'])
def user(id):
    app = Application()
    user = app.get_user_by_id(id)
    return render_template('profile.html', user=user)

@bp.route('/user/<int:id>/edit', methods=['POST', 'GET'])
def edit_user(id):
    app = Application()
    username = request.form.get('username')
    password = request.form.get('pwd')
    role = request.form.get('role')

    app.edit_user(id, username, role, password)
    session['role'] = role

    return redirect('/user/{}'.format(id))

@bp.route('/user/<int:id>/delete', methods=['POST', 'GET'])
def delete_user(id):
    app = Application()
    app.delete_user(id)
    session.clear()
    return redirect('/login')
