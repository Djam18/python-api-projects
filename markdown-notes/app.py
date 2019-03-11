from flask import Flask, request, jsonify
import sqlite3
from renderer import render

app = Flask(__name__)
DB = "notes.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            tags TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route('/notes', methods=['GET'])
def list_notes():
    conn = get_db()
    notes = conn.execute("SELECT id, title, tags, created_at FROM notes").fetchall()
    conn.close()
    return jsonify([dict(n) for n in notes])


@app.route('/notes', methods=['POST'])
def create_note():
    data = request.json
    tags = ','.join(data.get('tags', []))
    conn = get_db()
    conn.execute(
        "INSERT INTO notes (title, content, tags, created_at, updated_at) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
        (data.get('title', ''), data.get('content', ''), tags)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    conn = get_db()
    note = conn.execute("SELECT * FROM notes WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not note:
        return jsonify({"error": "not found"}), 404
    data = dict(note)
    data['html'] = render(data['content'] or '')
    return jsonify(data)


@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.json
    tags = ','.join(data.get('tags', []))
    conn = get_db()
    conn.execute(
        "UPDATE notes SET title=?, content=?, tags=?, updated_at=datetime('now') WHERE id=?",
        (data.get('title'), data.get('content'), tags, id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "updated"})


@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True, port=5005)
