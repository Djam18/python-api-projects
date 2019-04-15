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
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit
    conn = get_db()
    if status == 'done':
        todos = conn.execute("SELECT * FROM todos WHERE done=1 LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    elif status == 'pending':
        todos = conn.execute("SELECT * FROM todos WHERE done=0 LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    else:
        todos = conn.execute("SELECT * FROM todos LIMIT ? OFFSET ?", (limit, offset)).fetchall()
    conn.close()
    return jsonify([dict(t) for t in todos])


@app.route('/todos', methods=['POST'])
def create_todo():
    title = request.json.get('title')
    conn = get_db()
    conn.execute("INSERT INTO todos (title, done, created_at) VALUES (?, 0, datetime('now'))", (title,))
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
