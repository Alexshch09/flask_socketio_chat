from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from .extensions import conn, login_manager
from .test1 import main, socketio
from .auth import *
from .stats import *
from .list import *
from .guides import *
from .main_page import *


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True # Enable debug
    app.config["SECRET_KEY"] = "secret" # Secret key
    app.config["SESSION_TYPE"] = "filesystem"  # Storage for sessions

    login_manager.init_app(app)

    app.register_blueprint(main) # Test (1 question)
    app.register_blueprint(auth) # Auth (Login/Register)
    app.register_blueprint(stats)
    app.register_blueprint(lists)
    app.register_blueprint(guides)
    app.register_blueprint(lending)

    socketio.init_app(app) # Socket.io init

    Session(app) # Sessions init

    return app # Send app
