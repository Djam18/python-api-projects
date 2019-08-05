"""SQLAlchemy models for todo-api."""
from database import db
from datetime import datetime


class Todo(db.Model):
    """A single todo item."""

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Return dict representation."""
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": str(self.created_at),
        }
