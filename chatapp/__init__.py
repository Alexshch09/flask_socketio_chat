from flask import Flask
from flask_session import Session
from .test1 import main, socketio
from .auth import *


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret"
    app.config["SESSION_TYPE"] = "filesystem"  # You can change this as needed

    app.register_blueprint(main)
    app.register_blueprint(auth)

    socketio.init_app(app)

    Session(app)

    return app
