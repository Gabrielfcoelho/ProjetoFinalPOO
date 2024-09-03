import sqlite3

from flask import Blueprint, redirect, render_template, request, session

from flask_session import Session

from ..helpers.helpers import (admin_required, apology, get_stock,
                               login_required)
from ..models.stock import Stock
from ..models.user import User
from ..models.wallet import Wallet
from .application import Application
from .dataRecord import DataRecord

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
    new_user = app.register_user(username, password, admin)
    if not new_user:
        return apology('Usuário já utilizado')
    return redirect('/admin/login')

@bp.route('/admin/login', methods=["POST", "GET"])
def admin_login():
    if request.method == 'GET':
        adm = True
        return render_template('login.html', adm=adm)

    app = Application()
    username = request.form.get('username')
    password = request.form.get('pwd')
    user = app.db.get_user(username, password)

    print(user)
    session['user_id'] = user[0] 
    session['admin'] = user[3]

    return redirect('/admin')


@bp.route('/admin', methods=["GET", "POST"])
@admin_required
def admin_index():
    return render_template("index.html")



@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('pwd')

    app = Application()
    user = app.db.get_user(username, password)
    if not app.authenticate_user(username, password):
        return apology('Usuário não encontrado')
    
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
    if request.method == 'POST':
        q = request.form.get('symbol')

        stock = get_stock(q)
        return render_template('index.html', stock=stock)
    
    return render_template('index.html')


@bp.route('/buy', methods=['POST', 'GET'])
@login_required
def buy():
    if request.method == 'GET':
        return render_template('quote.html')
    
    q = request.form.get('symbol')
    stock = get_stock(q)
    if stock is None:
        return apology('Ação não encontrada', 404)
    
    return render_template('quote.html', stock=stock)

@bp.route("/buy", methods=['GET', 'POST'])
@login_required
def wallet():
    if request.method == 'GET':
        return render_template('buy.html')
    
    app = Application()
    wallet = Wallet()
    
    symbol = request.form.get('stock')
    qtd = float(request.form.get('qtd'))
    price = float(request.form.get('price'))

    if get_stock(symbol) is None:
        return apology('Ação não encontrada', 404)

    stock = Stock(symbol, price, qtd)

    #inserindo ações na carteira
    wallet.buy_stock(stock)
    #testando carteira
    print(wallet.stock_list)
    #inserindo mais ações
    price += 10
    stock = Stock(symbol, price, qtd)
    wallet.buy_stock(stock)
    #testando carteira
    print(wallet.stock_list)

    return redirect('/')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')