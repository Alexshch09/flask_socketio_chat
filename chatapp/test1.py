# One question test module for flask_test project
# On load render test page and creating an socket.io connection
# PostgreSQL connection in the extensions.py
# On next_question request choses an random question from database, saves session["question_id"] to user session and sends an question data to user
# On check_answer request, gets an answer data from user (A|B|C|D) and compares it to the questions from database with id from session['question_id], and sends result to user

from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import current_user
from .extensions import socketio, emit, conn 

main = Blueprint("main", __name__)

# Main one question test class
class Test_one:
    def __init__(self, theme):
        self.theme = theme

    def get_random_question(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Questions ORDER BY RANDOM() LIMIT 1")  # Get a random question from the database
            result = cursor.fetchone() # Fetch one question
            session["question_id"] = result[0] # Saving current question id to session

            return {"text": result[2], "a": result[4], "b": result[5], "c": result[6], "d": result[7]} # Return question data
    
    def check_user_answer(self, data):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Questions WHERE id = %s", (session["question_id"],)) # Compare answer and correct answer from session["question_id"]
            result = cursor.fetchone() # Fetch one question
            correct_answer = result[8] # result[8] - correct_answer

            return {"res": data == correct_answer, "cor_res": correct_answer, "your_ans": data}



exam_id = 1 # Exam type: 1 - INF03, 2 - INF02

# Creating an instance of the Test class
test = Test_one(exam_id)



# Main Page render
@main.route("/")
def index():
    return render_template("index.html") # Now it`s a page with Start test button


# Socket.io on Connect
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

# Socket.io on User Joins
@socketio.on("user_join")
def handle_user_join():
    print("User joined!")


# Handle next question
@socketio.on("next_question")
def handle_new_message():
    socketio.emit("get_question", test.get_random_question()) # Send question


# Handle answer check
@socketio.on("check_answer")
def handle_new_message(data):
    socketio.emit("check_complete", test.check_user_answer(data)) # send res: True/False, cor_res: Correct answer, your_ans: user answer 

