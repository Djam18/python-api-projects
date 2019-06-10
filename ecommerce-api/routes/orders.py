from flask import Blueprint, jsonify, request
import sqlite3
import os

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
    order_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "order created", "order_id": order_id, "total": total}), 201


@orders_bp.route('/orders/<int:order_id>/pay', methods=['POST'])
def pay_order(order_id):
    from services.payment import create_checkout_session
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    if not order:
        return jsonify({"error": "order not found"}), 404
    try:
        session = create_checkout_session(
            order_id,
            order['total'],
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel"
        )
        return jsonify({"checkout_url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@orders_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    from services.payment import handle_webhook
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
    event = handle_webhook(payload, sig_header, webhook_secret)
    if not event:
        return jsonify({"error": "invalid webhook"}), 400
    if event['type'] == 'checkout.session.completed':
        print(f"Payment succeeded for session: {event['data']['object']['id']}")
    return jsonify({"status": "ok"})
