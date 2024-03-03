from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .extensions import socketio, emit, conn
import markdown2
from psycopg2 import OperationalError  # Import OperationalError from psycopg2

main = Blueprint("main", __name__) # Blueprint init

# Main one question test class
class Test_one:
    def __init__(self, theme):
        self.theme = theme # 1 - INF02, 2 - INF03 (exam_id)

    def get_random_question(self):
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions WHERE exam_id = %s ORDER BY RANDOM() LIMIT 1", (self.theme,))
                result = cursor.fetchone()
                session["question_id"] = result[0]
                session["question_answered"] = False

                return {"id": result[0], "text": result[2], "a": result[4], "b": result[5], "c": result[6], "d": result[7]}
        except OperationalError as e:  # Handle database connection errors
            print("Database error:", e)
            return None

    def check_user_answer(self, data):
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Questions WHERE id = %s", (session["question_id"],))
                result = cursor.fetchone()
                correct_answer = result[8]
                self.stats_write(data)

                return {"res": data == correct_answer, "cor_res": correct_answer, "your_ans": data}
        except OperationalError as e:
            print("Database error:", e)
            return None

    def stats_write(self, data):
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Stats (user_id, exam_id, quest_id, answer) VALUES (%s, %s, %s, %s)",
                    (session["user_id"], self.theme, session["question_id"], data,))
                conn.commit()
        except OperationalError as e:
            print("Database error:", e)


exam_id = 1  # Exam type: 1 - INF03, 2 - INF02

# Creating an instance of the Test class
test = Test_one(exam_id)


# Main Page render
@main.route("/test")
@login_required
def index():
    if "user_id" not in session:
        flash("You need to be logged in to access the test.", "error")
        return redirect(url_for("auth.login"))
    else:
        return render_template("test1.html")


# Socket.io on Connect
@socketio.on("connect")
@login_required
def handle_connect():
    print("Client connected!")

@socketio.on('disconnect')
@login_required
def test_disconnect():
    print('Client disconnected')


# Handle next question
@socketio.on("next_question")
@login_required
def handle_new_message():
    question = test.get_random_question()
    if question:
        socketio.emit("get_question", question)
    else:
        socketio.emit("some_problem", "Error occurred while fetching question from the database")


# Handle answer check
@socketio.on("check_answer")
@login_required
def handle_new_message(data):
    if "question_answered" in session and "question_id" in session:
        if session["question_answered"] == False:
            session["question_answered"] = True
            result = test.check_user_answer(data)
            if result:
                socketio.emit("check_complete", result)
            else:
                socketio.emit("some_problem", "Error occurred while checking answer")
        else:
            socketio.emit("some_problem", "Question has already been answered")
    else:
        socketio.emit("reload_page", request.referrer)

# Send Stats to user
@socketio.on("send_stats")
@login_required
def handle_stats():
    try:
        if "question_answered" in session and "question_id" in session:
            user_id = session["user_id"]
            query = "SELECT s.answer, q.correct_answer, s.date AS question_text FROM Stats s JOIN Questions q ON s.quest_id = q.id WHERE s.user_id = %s AND s.quest_id = %s ORDER BY date DESC;"

            with conn.cursor() as cursor:
                cursor.execute(query, (user_id, session["question_id"],))
                stat_of_id = cursor.fetchall()

            data = []

            if stat_of_id:
                for a in stat_of_id:
                    b = [a[0], a[1]]
                    data.append(b)

                socketio.emit("get_stats", data)
            else:
                socketio.emit("get_stats_none")
        else:
            socketio.emit("reload_page", request.referrer)

    except OperationalError as e:
        print("Database error:", e)
        socketio.emit("some_problem", "Error occurred while fetching stats")


@socketio.on("send_guide")
@login_required
def handle_guide():
    try:
        if "question_answered" in session and "question_id" in session:
            query = "SELECT * FROM Guides WHERE question_id = %s LIMIT 1;"

            with conn.cursor() as cursor:
                cursor.execute(query, (session["question_id"],))
                guide = cursor.fetchall()

            if guide:
                print(guide)
                guide_text = markdown2.markdown(guide[0][2], extras=['fenced-code-blocks', 'mermaid'])
                print(guide_text)
                socketio.emit("get_guide", guide_text)
            else:
                socketio.emit("get_guide_none")
        else:
            socketio.emit("reload_page", request.referrer)
            
    except OperationalError as e:
        print("Database error:", e)
        socketio.emit("some_problem", "Error occurred while fetching guide")
