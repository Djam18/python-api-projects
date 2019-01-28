from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "todos.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            done INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route('/todos', methods=['GET'])
def list_todos():
    conn = get_db()
    todos = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return jsonify([dict(t) for t in todos])


@app.route('/todos', methods=['POST'])
def create_todo():
    title = request.json.get('title')
    # bug: sql injection possible here
    conn = get_db()
    conn.execute(f"INSERT INTO todos (title, done, created_at) VALUES ('{title}', 0, datetime('now'))")
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    conn = get_db()
    todo = conn.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not todo:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(todo))


@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE todos SET title=?, done=? WHERE id=?",
                 (data.get('title'), data.get('done', 0), id))
    conn.commit()
    conn.close()
    return jsonify({"message": "updated"})


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
