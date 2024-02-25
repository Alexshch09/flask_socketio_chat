from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from flask_login import current_user

auth = Blueprint("auth", __name__)

# PostgreSQL connection configuration
conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='root',
    database='egzamin'
)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username is already taken
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s", (username,))
            if cursor.fetchone():
                flash("Username already exists. Please choose a different one.", "error")
                return redirect(url_for("auth.register"))

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Save the user to the database
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()

        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieve user from the database
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s", (username,))
            user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]  # Store user id in session
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")

@auth.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You need to be logged in to access the dashboard.", "error")
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", current_user=current_user)

@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))