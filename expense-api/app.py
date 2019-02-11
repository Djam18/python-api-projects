from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "expenses.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            description TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route('/expenses', methods=['GET'])
def list_expenses():
    start = request.args.get('start')
    end = request.args.get('end')
    category = request.args.get('category')
    conn = get_db()
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if start:
        query += " AND date >= ?"
        params.append(start)
    if end:
        query += " AND date <= ?"
        params.append(end)
    if category:
        query += " AND category = ?"
        params.append(category)
    expenses = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(e) for e in expenses])


@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
        (data['amount'], data.get('category', 'other'), data.get('description', ''), data.get('date', ''))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True, port=5003)
