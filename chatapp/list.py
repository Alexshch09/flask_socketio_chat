from flask import Blueprint, render_template, session, redirect, url_for, flash
from .extensions import socketio, emit, conn 

lists = Blueprint("lists", __name__) # Blueprint init

@lists.route("/list")
def index():
    query = "SELECT * FROM Questions;"

    with conn.cursor() as cursor:
        cursor.execute(query)
        questions = cursor.fetchall()

        return render_template("list.html", data=questions)