import sqlite3

from flask import Blueprint, redirect, render_template, request

from ..helpers.helpers import apology, login_required
from ..models.user import User

# from .dataRecord import DataRecord

bp = Blueprint('main',__name__)

con = sqlite3.connect('app/controllers/db/site.db')
cur = con.cursor()

def adapter_user(user):
    return f'{user.username}; {user.password}'

sqlite3.register_adapter(User, adapter_user)

def new_user(username, password):
    data = User(username, password)
    cur.executemany("INSERT INTO users VALUES(?)", data)
    con.commit()
    return

@bp.route("/")
@login_required
def index():
    return render_template('layout.html')

@bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('pwd')
    return render_template('login.html', username=username, password=password)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    password = request.form.get('pwd')
    # Cria um novo usuário com os dados
    user = User(username, password)

    # Registra o usuário no banco de dados com a própria classe
    user.register()
    return redirect('/login')

    