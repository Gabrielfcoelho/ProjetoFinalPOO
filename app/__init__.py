from flask import Flask

from app.controllers import bp as main_bp
from app.controllers.application import Application


def create_app():
    app = Flask(__name__, )

    #Registrar blueprints
    app.register_blueprint(main_bp)

    return app


