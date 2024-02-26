from flask import Blueprint, render_template, session, redirect, url_for, flash
import random
from flask_login import current_user
from .extensions import socketio, emit, conn 

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
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Questions ORDER BY RANDOM() LIMIT 1")  # Get a random question from the database
        result = cursor.fetchone()

    session["question_id"] = result[0]

    socketio.emit("get_question", {"text": result[2], "a": result[4], "b": result[5], "c": result[6], "d": result[7]})

@socketio.on("check_answer")
def handle_new_message(data):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Questions WHERE id = %s", (session["question_id"],))
        result = cursor.fetchone()

    correct_answer = result[8]

    emit("check_complete", {"res": data == correct_answer, "cor_res": correct_answer, "your_ans": data})

