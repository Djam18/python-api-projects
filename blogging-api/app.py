from flask import Flask, request, jsonify
import sqlite3
from auth import init_auth_db, register_user, login_user, verify_token

app = Flask(__name__)
DB = "blog.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            author_id INTEGER,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()
init_auth_db()


def get_current_user():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    return verify_token(token)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        register_user(data['username'], data['password'], data.get('email', ''))
        return jsonify({"message": "registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    token = login_user(data['username'], data['password'])
    if not token:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"token": token})


@app.route('/posts', methods=['GET'])
def list_posts():
    conn = get_db()
    posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(p) for p in posts])


@app.route('/posts', methods=['POST'])
def create_post():
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO posts (title, content, author_id, created_at) VALUES (?, ?, ?, datetime('now'))",
        (data['title'], data.get('content', ''), user['user_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    conn = get_db()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not post:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(post))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
