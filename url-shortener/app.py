from flask import Flask, request, jsonify, redirect
import sqlite3
from shortener import generate_code

app = Flask(__name__)
DB = "urls.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    url = data.get('url')
    if not url:
        return jsonify({"error": "url required"}), 400
    code = generate_code()
    conn = get_db()
    conn.execute(
        "INSERT INTO urls (original_url, short_code, created_at) VALUES (?, ?, datetime('now'))",
        (url, code)
    )
    conn.commit()
    conn.close()
    return jsonify({"short_url": f"http://localhost:5004/{code}", "code": code}), 201


@app.route('/<code>')
def redirect_url(code):
    conn = get_db()
    row = conn.execute("SELECT * FROM urls WHERE short_code = ?", (code,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "not found"}), 404
    conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,))
    conn.commit()
    conn.close()
    return redirect(row['original_url'])


@app.route('/stats/<code>')
def stats(code):
    conn = get_db()
    row = conn.execute("SELECT * FROM urls WHERE short_code = ?", (code,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(row))


if __name__ == '__main__':
    app.run(debug=True, port=5004)
