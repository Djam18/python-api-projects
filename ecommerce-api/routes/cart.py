from flask import Blueprint, jsonify, request
import sqlite3

cart_bp = Blueprint('cart', __name__)
DB = "ecommerce.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@cart_bp.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.headers.get('X-User-Id', 1)
    conn = get_db()
    items = conn.execute("""
        SELECT c.*, p.name, p.price FROM cart_items c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,)).fetchall()
    conn.close()
    total = sum(item['price'] * item['quantity'] for item in items)
    return jsonify({"items": [dict(i) for i in items], "total": total})


@cart_bp.route('/cart', methods=['POST'])
def add_to_cart():
    user_id = request.headers.get('X-User-Id', 1)
    data = request.json
    conn = get_db()
    existing = conn.execute("SELECT * FROM cart_items WHERE user_id=? AND product_id=?",
                            (user_id, data['product_id'])).fetchone()
    if existing:
        conn.execute("UPDATE cart_items SET quantity=quantity+? WHERE user_id=? AND product_id=?",
                     (data.get('quantity', 1), user_id, data['product_id']))
    else:
        conn.execute("INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)",
                     (user_id, data['product_id'], data.get('quantity', 1)))
    conn.commit()
    conn.close()
    return jsonify({"message": "added to cart"}), 201
