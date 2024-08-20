from flask import Flask, request, render_template
from app.controllers.application import Application
from markupsafe import escape
from helpers.helpers import login_required

app = Flask(__name__)
ctl = Application()


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return render_template('index.html')
    return render_template('login.html')



if __name__ == "__main__":
    app.run(debug=True)
