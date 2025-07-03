from app.config.db import db
from uuid import uuid4


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    id = db.Column(db.UUID, primary_key=True, unique=True, default=uuid4)
    email = db.Column(db.VARCHAR, unique=True)

    account = db.relationship(
        "Account", back_populates="user", cascade="all, delete")
