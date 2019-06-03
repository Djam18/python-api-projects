from flask import Blueprint, jsonify, request
import sqlite3

products_bp = Blueprint('products', __name__)
DB = "ecommerce.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@products_bp.route('/products', methods=['GET'])
def list_products():
    category = request.args.get('category')
    conn = get_db()
    if category:
        products = conn.execute("SELECT * FROM products WHERE category = ?", (category,)).fetchall()
    else:
        products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])


@products_bp.route('/products', methods=['POST'])
def create_product():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO products (name, price, stock, category) VALUES (?, ?, ?, ?)",
        (data['name'], data['price'], data.get('stock', 0), data.get('category', ''))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "created"}), 201


@products_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (id,)).fetchone()
    conn.close()
    if not product:
        return jsonify({"error": "not found"}), 404
    return jsonify(dict(product))


@products_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    conn = get_db()
    conn.execute("UPDATE products SET name=?, price=?, stock=? WHERE id=?",
                 (data.get('name'), data.get('price'), data.get('stock'), id))
    conn.commit()
    conn.close()
    return jsonify({"message": "updated"})


@products_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "deleted"})
