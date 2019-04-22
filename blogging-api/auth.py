import jwt
import sqlite3
import bcrypt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

SECRET_KEY = os.environ.get("JWT_SECRET", "fallback-secret-not-for-prod")
DB = "blog.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def register_user(username, password, email):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db()
    conn.execute(
        "INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, datetime('now'))",
        (username, hashed.decode('utf-8'), email)
    )
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if not user:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return None
    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, SECRET_KEY, algorithm='HS256')
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except Exception:
        return None
