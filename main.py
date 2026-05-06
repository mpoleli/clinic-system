from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL)

# ================= INIT =================
def init():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT,
            user_type TEXT DEFAULT 'student'
        )
    """)

    conn.commit()
    cur.close()
    conn.close()

init()

# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, email, password, user_type) VALUES (%s, %s, %s, %s)",
            (data["username"], data["email"], data["password"], "student")
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cur.close()
        conn.close()

# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, user_type FROM users WHERE email=%s AND password=%s",
        (data["email"], data["password"])
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user[0],
            "username": user[1],
            "user_type": user[2]
        })

    return jsonify({"error": "Invalid credentials"}), 401


# ================= RUN =================
if __name__ == "__main__":
    app.run()
