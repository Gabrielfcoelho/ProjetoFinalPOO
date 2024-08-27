from flask import Flask
from flask_session import Session

# from app.controllers.dataRecord import DataRecord
from app.controllers import bp as main_bp
from app.controllers import db
from app.controllers.application import Application


def create_app():
    app = Flask(__name__, )
    
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    #Conectar banco de dados


    #Registrar blueprints
    app.register_blueprint(main_bp)

    return app


