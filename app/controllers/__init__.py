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
    return redirect('/admin/login')


@bp.route('/admin/login', methods=["POST", "GET"])
def admin_login():
    if request.method == 'GET':
        adm = True
        return render_template('login.html', adm=adm)

    app = Application()
    username = request.form.get('username')
    password = request.form.get('pwd')
    user = app.get_user(username, password)

    print(user)
    session['user_id'] = user[0] 
    session['admin'] = user[3]

    return redirect('/admin')


@bp.route('/admin', methods=["GET", "POST"])
@admin_required
def admin_index():
    app = Application()
    
    users = app.db.get_all_users()
    wallets = app.db.get_all_wallet()
    # history = db.execute("SELECT * FROM history")

    return render_template("admin.html", users=users, wallets=wallets)


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
    
    print(user)

    session['user_id'] = user[0] 
    session['admin'] = user[3]

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
    print(wallet)
    
    return render_template('index.html', wallet=wallet)

# comprar stocks
@bp.route("/buy", methods=['GET', 'POST'])
@login_required
def buy():
    if request.method == 'GET':
        return render_template('buy.html')
    
    app = Application()
    
    symbol = request.form.get('stock')
    qtd = float(request.form.get('qtd'))
    price = get_stock(symbol)['price']

    if get_stock(symbol) is None:
        return apology('Ação não encontrada', 404)
    
    app.buy_stock(symbol, qtd, price, session["user_id"])

    return redirect('/')

# vender stocks
@bp.route("/sell", methods= ["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        return render_template("sell.html")
    
    app = Application()

    symbol = request.form.get('stock')
    qtd = float(request.form.get('qtd'))
    price = get_stock(symbol)['price']

    if app.sell_stock(symbol, qtd, price, session["user_id"]) is not True:
        return apology("Operação inválida!")

    return redirect("/")

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

@bp.route('/user/<int:id>/edit', methods=['POST'])
def edit_user(id):
    app = Application()
    username = request.form.get('username')
    password = request.form.get('pwd')
    role = request.form.get('role')

    app.edit_user(id, username, role, password)
    return redirect('/user/{}'.format(id))

@bp.route('/user/<int:id>/delete', methods=['POST'])
def delete_user(id):
    app = Application()
    app.delete_user(id)
    session.clear()
    return redirect('/login')
