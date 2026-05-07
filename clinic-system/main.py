from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# ================= DATABASE =================
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL)

# ================= INIT DB =================
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database ready")

init_db()

# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        username = data["username"]
        email = data["email"]
        password = data["password"]

        # ROLE LOGIC
        if email == "admin@bothouniversityclinic.ac.bw":
            role = "ADMIN"
        elif email.endswith("@bothouniversity.ac.bw"):
            role = "LECTURER"
        else:
            role = "STUDENT"

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (username, email, password, role))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User registered successfully"})

    except psycopg2.errors.UniqueViolation:
        return jsonify({"message": "Email already exists"}), 400

    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, username, email, role
            FROM users
            WHERE email=%s AND password=%s
        """, (email, password))

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3],
                "message": "Login successful"
            })

        return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"message": "Server error", "error": str(e)}), 500


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
