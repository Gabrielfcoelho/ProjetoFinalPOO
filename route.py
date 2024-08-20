from flask import Flask, request, render_template
from app.controllers.application import Application
from markupsafe import escape

app = Flask(__name__)
ctl = Application()

@app.route

@app.route("/")
@app.route("/login")
def login():
    return render_template('layout.html')

if __name__ == "__main__":
    app.run(debug=True)
