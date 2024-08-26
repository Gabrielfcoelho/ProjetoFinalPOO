import sqlite3

from flask import Blueprint, redirect, render_template, request

from .dataRecord import DataRecord
from ..helpers.helpers import apology, login_required
from ..models.user import User

#instanciando blueprint
bp = Blueprint('main',__name__)

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

    