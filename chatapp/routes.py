from flask import Blueprint, render_template
from flask import request
from .extensions import socketio, emit

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join():
    print("User joined!")

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None
    emit("chat", {"message": message, "username": username}, broadcast=True)