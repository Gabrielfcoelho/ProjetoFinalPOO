from flask import Blueprint, render_template, request

from ..helpers.helpers import login_required, apology

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