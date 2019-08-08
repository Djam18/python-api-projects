"""SQLAlchemy models for blogging-api."""
from database import db
from datetime import datetime


class Post(db.Model):
    """A blog post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, default="")
    author_id = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(500), default="")  # comma separated - not ideal but ok for now
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict:
        """Return dict representation."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.author_id,
            "tags": self.tags.split(",") if self.tags else [],
            "created_at": str(self.created_at),
        }
