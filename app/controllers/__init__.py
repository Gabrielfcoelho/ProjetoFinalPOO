import sqlite3

from flask import Blueprint, redirect, render_template, request, session

from flask_session import Session

from ..helpers.helpers import apology, login_required
from ..models.user import User
from ..models.stock import Stock
from .dataRecord import DataRecord
from .application import Application

#instanciando blueprint
bp = Blueprint('main', __name__)


@bp.route("/")
@login_required
def index():
    return render_template('index.html')

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
    
    print(user)
    session['user_id'] = user[0] 

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

@bp.route("/wallet", methods=['GET', 'POST'])
def wallet():
    if request.method == 'GET':
        return render_template('wallet.html')
    app = Application()
    stockName = request.form.get('stock')
    qtd = float(request.form.get('qtd'))
    price = float(request.form.get('price'))
    stock = Stock(stockName, price, qtd)
    #inserindo carteira no banco de dados
    app.db.update_wallet(stock)
    #testando carteira
    print(app.db.show_wallet())
    return redirect('/')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')