# Authentication module for flask_test project
# Takes data from template form and puts it to postgresql database
# PostgreSQL connection in the extensions.py
# Four methods:
#   /register (gets data from form, checks if username is already taken, hashing password, and saves data to database (egzamin:user), after redirects user to login page)
#   /login (gets data from form, checks if user exists, checks password, if correct redirects to dashboard, if false gets error, user id is stored in the session["user_id"])
#   /dashboard (Checks if user_id exists, if true loads an dashboard, else redirects to login page)
#   /logout (Deletes an user_id from session, redirects to the login page)

from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from .extensions import conn

auth = Blueprint("auth", __name__)


# Registration Function Get - Page, Post - form data
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")  # username from form
        password = request.form.get("password")  # password from form

        # Check if username is already taken
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s", (username,))
            if cursor.fetchone():
                flash(
                    "Username already exists. Please choose a different one.", "error"
                )
                return redirect(url_for("auth.register"))

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Save the user to the database
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (login, password, email, nickname) VALUES (%s, %s, %s, %s)",
                (username, hashed_password, "test1@test.com", "nickname"),
            )
            conn.commit()

        # Registration succesfull

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    # Render Registration Page
    return render_template("register.html")


# Login Function Get - Page, Post - form data
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")  # username from form
        password = request.form.get("password")  # password from form

        # Retrieve user from the database
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE login = %s", (username,)
            )  # Check username
            user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]  # Store user id in session
            flash("Login successful!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")


# Dashboard Page
@auth.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You need to be logged in to access the dashboard.", "error")
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", current_user=current_user)


# Logout
@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
