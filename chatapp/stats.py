from flask import Blueprint, render_template, session, redirect, url_for, flash
from .extensions import conn 

stats = Blueprint("stats", __name__) # Blueprint init

@stats.route("/stats")
def index():
    if "user_id" not in session:
        flash("You need to be logged in to access your stats.", "error") # User is not logged
        return redirect(url_for("auth.login"))
    else:
        # Get the user's ID from the session
        user_id = session["user_id"]
        
        # Execute SQL query to retrieve stats for the current user
        query = "SELECT user_id, exam_id, quest_id, answer, date FROM Stats WHERE user_id = %s;"

        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            user_stats = cursor.fetchall()

        # Render the template and pass the stats data to it
        return render_template("stats.html", stats=user_stats)

@stats.route("/stat/<int:id>")
def one_stat(id):
    user_id = session["user_id"] 
        
    # Execute SQL query to retrieve stats for the current user
    query = "SELECT user_id, exam_id, quest_id, answer, date FROM Stats WHERE user_id = %s AND quest_id = %s;"

    with conn.cursor() as cursor:
        cursor.execute(query, (user_id, id,))
        stat_of_id = cursor.fetchall()
    
    return render_template("one_stat.html", stats=stat_of_id)