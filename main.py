from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# ================= CORS (IMPORTANT FOR HTML/JS) =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all devices (hosting safe)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= DATABASE =================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    username TEXT,
    user_type TEXT,
    last_login TEXT
)
""")
conn.commit()

# ================= REQUEST MODEL =================
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# ================= REGISTER =================
@app.post("/register")
def register(user: UserRegister):
    try:
        cursor.execute(
            "INSERT INTO users (email, password, username, user_type, last_login) VALUES (?, ?, ?, ?, ?)",
            (
                user.email,
                user.password,
                user.username,
                "student",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()

        return {"message": "User registered successfully"}

    except sqlite3.IntegrityError:
        return {"error": "Email already registered"}

    except Exception as e:
        return {"error": str(e)}


# ================= LOGIN =================
@app.post("/login")
def login(user: UserLogin):
    cursor.execute(
        "SELECT id, username, user_type FROM users WHERE email=? AND password=?",
        (user.email, user.password)
    )
    result = cursor.fetchone()

    if result:
        return {
            "message": "Login successful",
            "user_id": result[0],
            "username": result[1],
            "user_type": result[2]
        }

    return {"error": "Invalid email or password"}


# ================= TEST =================
@app.get("/")
def home():
    return {"message": "Backend is running successfully"}