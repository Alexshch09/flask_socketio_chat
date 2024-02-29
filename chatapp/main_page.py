from flask import Blueprint, render_template, session, redirect, url_for, flash
from .extensions import socketio, emit, conn 

lending = Blueprint("lending", __name__) # Blueprint init

@lending.route("/")
def index():
    if "user_id" not in session:
        flash("You need to be logged in to access the dashboard.", "error")
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html")