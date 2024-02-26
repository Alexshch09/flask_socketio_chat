from flask import Blueprint, render_template, session, redirect, url_for, flash
from .extensions import socketio, emit, conn 
import markdown2

guides = Blueprint("guides", __name__) # Blueprint init

@guides.route("/guides/<int:id>")
def index(id):
    if "user_id" not in session:
        flash("You need to be logged in to access your stats.", "error") # User is not logged
        return redirect(url_for("auth.login"))
    
    else:
        # Execute SQL query to retrieve stats for the current user
        query = "SELECT * FROM Guides WHERE question_id = %s;"

        with conn.cursor() as cursor:
            cursor.execute(query, (id,))
            guide = cursor.fetchall()
        
        if not guide:
            return render_template("guide_not_exists.html", data = guide)
        else:
            # Assuming guide is a tuple containing dictionaries, access the first element of the tuple
            guide_text = markdown2.markdown(guide[0][2])

            # Render the template and pass the converted HTML
            return render_template("guide.html", title=guide[0][1], author=guide[0][3], text=guide_text)
