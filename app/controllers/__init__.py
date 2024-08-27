import sqlite3

from flask import Blueprint, redirect, render_template, request, session

from flask_session import Session

from ..helpers.helpers import apology, get_stock, login_required
from ..models.user import User
from .dataRecord import DataRecord

#instanciando blueprint
bp = Blueprint('main', __name__)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'POST':
        q = request.form.get('symbol')

        stock = get_stock(q)
        return render_template('index.html', stock=stock)
    
    return render_template('index.html')

@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('pwd')

    db = DataRecord()
    user = db.get_user(username, password)
    if user is None:
        return apology('Usuário não encontrado')
    
    print(user)
    session['user_id'] = user[0] 

    return redirect('/')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    #conectando com banco de dados
    db = DataRecord()
    #coletando dados
    username = request.form.get('username')
    password = request.form.get('pwd')
    #instanciando objeto User
    user = User(username, password)
    #adicionando user ao banco de dados
    db.new_user(user)
    return redirect('/login')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')