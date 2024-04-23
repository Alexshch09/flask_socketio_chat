from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from .extensions import conn, login_manager
from .auth import *
from .main_page import *


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True # Enable debug
    app.config["SECRET_KEY"] = "secret" # Secret key
    app.config["SESSION_TYPE"] = "filesystem"  # Storage for sessions

    login_manager.init_app(app)

    app.register_blueprint(auth) # Auth (Login/Register)
    app.register_blueprint(lending)

    Session(app) # Sessions init

    return app # Send app
