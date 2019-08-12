"""SQLAlchemy models for ecommerce-api."""
from database import db
from datetime import datetime


class Product(db.Model):
    """A product in the catalog."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(100), default="")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
        }


class CartItem(db.Model):
    """An item in a user's cart."""

    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product', lazy='joined')

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
        }


class Order(db.Model):
    """A completed order."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total": self.total,
            "status": self.status,
            "created_at": str(self.created_at),
        }
