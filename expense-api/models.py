"""SQLAlchemy models for expense-api."""
from database import db
from datetime import datetime


class Expense(db.Model):
    """An expense record."""

    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), default="")
    description = db.Column(db.String(500), default="")
    date = db.Column(db.String(20), default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Return dict representation."""
        return {
            "id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }
