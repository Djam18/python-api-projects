from flask import Flask
import sqlite3
from routes.products import products_bp
from routes.cart import cart_bp
from routes.orders import orders_bp

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-this'
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)
DB = "ecommerce.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            stock INTEGER DEFAULT 0,
            category TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            quantity INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL,
            status TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5009)
