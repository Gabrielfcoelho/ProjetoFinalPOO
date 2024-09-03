import datetime
from functools import wraps

import requests
from flask import redirect, render_template, session


# Função para renderizar mensagens de erro
def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


# Decorador para enviar usuário para o login caso não esteja logado
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Decorador para enviar erro ao usuário caso não seja admin
def admin_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin") is None:
            return apology("Usuário não tem permissão para acessar esta rota")
        return f(*args, **kwargs)

    return decorated_function


def get_stock(symbol):
    # Função para pegar informações de uma ação
    symbol = symbol.upper()
    url = f"http://brapi.dev/api/quote/{symbol}?token=tVvVt6GbrSWFeB5Sg34bd7"

    try:
        response = requests.get(url)
        response.raise_for_status()

        quote = response.json()
        price = round(float(quote["results"][-1]["regularMarketPrice"]), 2)
        return {"symbol": symbol, "price": price}
    except requests.RequestException:
        return None