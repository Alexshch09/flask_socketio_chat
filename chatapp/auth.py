from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import conn, login_manager
from .models import User

auth = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username already exists
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE login = %s", (username,))
            if cursor.fetchone():
                flash("Username already exists. Please choose a different one.", "error")
                return redirect(url_for("auth.register"))

        # Hash the password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Save the user to the database
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (login, password, email, nickname) VALUES (%s, %s, %s, %s)", (username, hashed_password, "hi1@hi.com", "test1111")
            )
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
            user_data = cursor.fetchone()

        if user_data and check_password_hash(user_data[2], password):
            user = User(user_id=user_data[0])
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")
