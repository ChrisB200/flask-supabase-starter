from app.config.db import db
from uuid import uuid4


class Account(db.Model):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.UUID, primary_key=True, unique=True, default=uuid4)
    name = db.Column(db.VARCHAR)
    user_id = db.Column(db.UUID, db.ForeignKey(
        "auth.users.id"), nullable=False)

    user = db.relationship(
        "User", back_populates="account", cascade="all, delete")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id
        }
