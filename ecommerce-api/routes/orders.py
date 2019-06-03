from flask import Blueprint, jsonify, request
import sqlite3

orders_bp = Blueprint('orders', __name__)
DB = "ecommerce.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@orders_bp.route('/orders', methods=['GET'])
def list_orders():
    user_id = request.headers.get('X-User-Id', 1)
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(o) for o in orders])


@orders_bp.route('/orders', methods=['POST'])
def create_order():
    user_id = request.headers.get('X-User-Id', 1)
    conn = get_db()
    cart_items = conn.execute("""
        SELECT c.*, p.price FROM cart_items c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    """, (user_id,)).fetchall()

    if not cart_items:
        return jsonify({"error": "cart is empty"}), 400

    total = sum(item['price'] * item['quantity'] for item in cart_items)
    conn.execute("INSERT INTO orders (user_id, total, status, created_at) VALUES (?, ?, 'pending', datetime('now'))",
                 (user_id, total))
    conn.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "order created", "total": total}), 201
