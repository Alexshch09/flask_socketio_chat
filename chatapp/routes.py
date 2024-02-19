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

@socketio.on("next_question")
def handle_new_message():
    emit("get_question", {"message": "a", "username": "b"})

@socketio.on("check_answer")
def handle_new_message(data):
    emit("check_complete", {"res":data=="B", "cor_res":"B", "your_ans":data})