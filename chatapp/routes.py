from flask import Blueprint, render_template
from flask import request, jsonify
from .extensions import socketio, emit
from flask import jsonify
import psycopg2
import random

main = Blueprint("main", __name__)

conn = psycopg2.connect(
    dbname="egzamin",
    user="postgres",
    password="root",
    host="127.0.0.1",
    port="5432"
    )

@main.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join():
    print("User joined!")
    id = random.randint(1, 1030)
    cur = conn.cursor()
    cur.execute("SELECT id, question_text, image_url, option_a, option_b, option_c, option_d FROM questions WHERE id = %s", (id,))
    rows = cur.fetchone()
    cur.close()
    
    row = {
            'id': rows[0],
            'question_text': rows[1],
            'image_url': rows[2],
            'option_a': rows[3],
            'option_b': rows[4],
            'option_c': rows[5],
            'option_d': rows[6]
        }
    emit("get_question", row)

@socketio.on("next_question")
def handle_new_message():
    id = random.randint(1, 1030)
    cur = conn.cursor()
    cur.execute("SELECT id, question_text, image_url, option_a, option_b, option_c, option_d FROM questions WHERE id = %s", (id,))
    rows = cur.fetchone()
    cur.close()
    
    row = {
            'id': rows[0],
            'question_text': rows[1],
            'image_url': rows[2],
            'option_a': rows[3],
            'option_b': rows[4],
            'option_c': rows[5],
            'option_d': rows[6]
        }
    emit("get_question", row)

@socketio.on("check_answer")
def handle_new_message(data):
    emit("check_complete", {"res":data=="B", "cor_res":"B", "your_ans":data})