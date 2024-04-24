from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from .extensions import conn 
from flask_login import login_required, current_user

test = Blueprint("test", __name__) # Blueprint init

@test.route("/api/download_answers")
@login_required
def show_test():
    connection = conn.cursor()

    # Fetch all questions from the database
    connection.execute("SELECT * FROM Questions;")
    questions = connection.fetchall()

    # Define a list to store serialized questions
    serialized_questions = []

    # Serialize each question and append to the list
    for question in questions:
        serialized_question = {
            "id": question[0],
            "exam_id": question[1],
            "text": question[2],
            "image": question[3].tobytes().decode('utf-8') if question[3] else None,
            "a": question[4],
            "b": question[5],
            "c": question[6],
            "d": question[7],
            "correct_answer": question[8]
        }
        serialized_questions.append(serialized_question)

    # Close the database connection
    connection.close()

    # Return the JSON response
    return jsonify(serialized_questions)