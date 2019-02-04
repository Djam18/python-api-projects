import jwt
import sqlite3
from datetime import datetime, timedelta

SECRET_KEY = "my-super-secret-key-1234"
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
    conn = get_db()
    # storing plaintext password - bad practice but works for now
    conn.execute(
        "INSERT INTO users (username, password, email, created_at) VALUES (?, ?, ?, datetime('now'))",
        (username, password, email)
    )
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    ).fetchone()
    conn.close()
    if not user:
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
