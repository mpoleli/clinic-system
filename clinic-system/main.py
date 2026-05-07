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

    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )


# ================= INIT DATABASE (SAFE) =================
def init_db():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # SAFE TABLE CREATION (NO DROP)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'STUDENT'
            );
        """)

        conn.commit()
        print("Database ready")

    except Exception as e:
        print("DATABASE INIT ERROR:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# ================= HOME =================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Clinic API is running"
    })


# ================= REGISTER =================
@app.route("/register", methods=["POST"])
def register():

    conn = None
    cur = None

    try:
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # VALIDATION
        if not username or not email or not password:
            return jsonify({
                "message": "All fields are required"
            }), 400

        # ROLE LOGIC
        if email == "admin@bothouniversityclinic.ac.bw":
            role = "ADMIN"
        elif email.endswith("@bothouniversity.ac.bw"):
            role = "LECTURER"
        else:
            role = "STUDENT"

        conn = get_db_connection()
        cur = conn.cursor()

        # CHECK EXISTING EMAIL
        cur.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        if cur.fetchone():
            return jsonify({
                "message": "Email already exists"
            }), 400

        # INSERT USER
        cur.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (username, email, password, role))

        conn.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except Exception as e:

        print("REGISTER ERROR:", e)

        if conn:
            conn.rollback()

        return jsonify({
            "message": "Server error",
            "error": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():

    conn = None
    cur = None

    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({
                "message": "Email and password required"
            }), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, username, email, role
            FROM users
            WHERE email=%s AND password=%s
        """, (email, password))

        user = cur.fetchone()

        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "role": user[3],
                "message": "Login successful"
            })

        return jsonify({
            "message": "Invalid credentials"
        }), 401

    except Exception as e:

        print("LOGIN ERROR:", e)

        return jsonify({
            "message": "Server error",
            "error": str(e)
        }), 500

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# ================= RUN =================
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
