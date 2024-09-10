from flask import Flask

# from app.controllers.dataRecord import DataRecord
from app.controllers import bp as main_bp
from flask_session import Session


def create_app():
    app = Flask(__name__, )
    
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    #Registrar blueprints
    app.register_blueprint(main_bp)

    return app


