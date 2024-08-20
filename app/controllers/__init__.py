from flask import Blueprint, render_template, request

bp = Blueprint('main',__name__)

@bp.route("/")
def index():
    return render_template('layout.html')

@bp.route('/login', methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('pwd')
    return render_template('layout.html', username=username, password=password)