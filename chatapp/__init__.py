from flask import Flask
from flask_session import Session
from .test1 import main, socketio
from .auth import *


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True # Enable debug
    app.config["SECRET_KEY"] = "secret" # Secret key
    app.config["SESSION_TYPE"] = "filesystem"  # Storage for sessions

    app.register_blueprint(main) # Test (1 question)
    app.register_blueprint(auth) # Auth (Login/Register)

    socketio.init_app(app) # Socket.io init

    Session(app) # Sessions init

    return app # Send app
