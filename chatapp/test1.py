# One question test module for flask_test project
# On load render test page and creating an socket.io connection
# PostgreSQL connection in the extensions.py
# On next_question request choses an random question from database, saves session["question_id"] to user session and sends an question data to user
# On check_answer request, gets an answer data from user (A|B|C|D) and compares it to the questions from database with id from session['question_id], and sends result to user

from flask import Blueprint, render_template, session, redirect, url_for, flash
from .extensions import socketio, emit, conn 
import markdown2

main = Blueprint("main", __name__) # Blueprint init

# Main one question test class
class Test_one:
    def __init__(self, theme):
        self.theme = theme # 1 - INF02, 2 - INF03 (exam_id)

    def get_random_question(self):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Questions WHERE exam_id = %s ORDER BY RANDOM() LIMIT 1", (self.theme,))  # Get a random question from the database
            result = cursor.fetchone() # Fetch one question
            session["question_id"] = result[0] # Saving current question id to session

            return {"id": result[0], "text": result[2], "a": result[4], "b": result[5], "c": result[6], "d": result[7]} # Return question data
    
    def check_user_answer(self, data):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Questions WHERE id = %s", (session["question_id"],)) # Compare answer and correct answer from session["question_id"]
            result = cursor.fetchone() # Fetch one question
            correct_answer = result[8] # result[8] - correct_answer
            self.stats_write(data) # Write statistics

            return {"res": data == correct_answer, "cor_res": correct_answer, "your_ans": data} # Send res: True/False, cor_res: Correct answer, your_ans: user answer 
    
    def stats_write(self, data):
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Stats (user_id, exam_id, quest_id, answer) VALUES (%s, %s, %s, %s)", 
                            (session["user_id"], self.theme, session["question_id"], data,)) 
                # Compare answer and correct answer from session["question_id"]
            
            conn.commit()



exam_id = 1 # Exam type: 1 - INF03, 2 - INF02

# Creating an instance of the Test class
test = Test_one(exam_id)


# Main Page render
@main.route("/test")
def index():
    if "user_id" not in session:
        flash("You need to be logged in to access the test.", "error") # User is not logged
        return redirect(url_for("auth.login"))
    else:
        # Render testing page
        return render_template("test1.html") # Now it`s a page with Start test button


# Socket.io on Connect
@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

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
    socketio.emit("check_complete", test.check_user_answer(data)) # Send res: True/False, cor_res: Correct answer, your_ans: user answer 

@socketio.on("send_stats")
def handle_stats():
    user_id = session["user_id"]
        
    # Execute SQL query to retrieve stats for the current user
    query = "SELECT s.answer, q.correct_answer, s.date AS question_text FROM Stats s JOIN Questions q ON s.quest_id = q.id WHERE s.user_id = %s AND s.quest_id = %s ORDER BY date DESC;"

    with conn.cursor() as cursor:
        cursor.execute(query, (user_id, 4,))
        stat_of_id = cursor.fetchall()

    data = []

    if stat_of_id:
        for a in stat_of_id:
            b = [a[0],a[1]]
            data.append(b)

        socketio.emit("get_stats", data)

    else:
        socketio.emit("get_stats_none")



@socketio.on("send_guide")
def handle_guide():
    query = "SELECT * FROM Guides WHERE question_id = %s LIMIT 1;"
    
    with conn.cursor() as cursor:
        cursor.execute(query, (session["question_id"],))
        guide = cursor.fetchall()

    if guide:
        guide_text = markdown2.markdown(guide[0][2])
        socketio.emit("get_guide", guide_text)
    else:
        socketio.emit("get_guide_none")