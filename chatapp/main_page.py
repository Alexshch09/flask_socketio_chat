from flask import Blueprint, render_template, session, redirect, url_for, flash
from .extensions import conn 
from flask_login import login_required, current_user

lending = Blueprint("lending", __name__) # Blueprint init

@lending.route("/")
@login_required
def index():
    return render_template("dashboard.html")