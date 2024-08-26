from flask import Flask
from app.controllers.dataRecord import DataRecord
from app.controllers import bp as main_bp
from app.controllers import db
from app.controllers.application import Application

def create_app():
    app = Flask(__name__, )

    #Conectar banco de dados


    #Registrar blueprints
    app.register_blueprint(main_bp)

    return app


