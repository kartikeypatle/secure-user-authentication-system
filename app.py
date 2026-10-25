import os
import sqlite3
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from datetime import datetime, timezone
from flask_bcrypt import Bcrypt

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("Secret key is missing")

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False

csrf = CSRFProtect(app)

bcrypt = Bcrypt(app)

DATABASE = "users.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def home():
    return render_template(
        "signup.html",
        csrf_token=generate_csrf()
    )

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
     return jsonify({"error": "Email and password must be strings"}), 400

    email = email.strip().lower()

    # Validate email
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        return jsonify({"error": "Enter a valid email"}), 400

    # Validate password
    if (
        len(password) < 8
        or not any(char.isdigit() for char in password)
        or not any(not char.isalnum() for char in password)
    ):
        return jsonify({
            "error": "Password must contain at least 8 characters, "
                     "one number and one special character"
        }), 400

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    connection = get_db_connection()

    try:
        connection.execute(
            """
            INSERT INTO users (email, password_hash, created_at)
            VALUES (?, ?, ?)
            """,
            (
                email,
                password_hash,
                datetime.now(timezone.utc).isoformat()
            )
        )

        connection.commit()

        return jsonify({
            "message": "Registration successful"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409

    finally:
        connection.close()
        
@app.route("/login", methods=["GET"])
@app.route("/login", methods=["GET"])
def login_page():
    return render_template(
        "login.html",
        csrf_token=generate_csrf()
    )

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request data"}), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
     return jsonify({"error": "Email and password must be strings"}), 400

    email = email.strip().lower()
    if not email or not isinstance(password, str) or not password:
        return jsonify({"error": "Email and password are required"}), 400

    connection = get_db_connection()

    try:
        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user is None or not bcrypt.check_password_hash(
            user["password_hash"], password
        ):
            return jsonify({"error": "Invalid email or password"}), 401
        session ["user_id"] = user["id"]
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "email": user["email"]
            }
        }), 200

    finally:
        connection.close()
        
@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return jsonify({"error": "Please login first"}), 401

    connection = get_db_connection()

    try:
        user = connection.execute(
            "SELECT id, email FROM users WHERE id = ?",
            (session["user_id"],)
        ).fetchone()

        if user is None:
            session.clear()
            return jsonify({"error": "User not found"}), 401

        return render_template(
            "dashboard.html",
            user=user,
            csrf_token=generate_csrf()
        )

    finally:
        connection.close()

@app.route("/logout", methods=["POST"])
def logout():
    if "user_id" not in session:
     return redirect(url_for("login_page"))      
    session.clear()

    return jsonify({
        "message": "Logout successful"
    }), 200

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)