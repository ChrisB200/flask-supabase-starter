from app.config.db import db, get_uuid


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    id = db.Column(db.UUID, primary_key=True, unique=True, default=get_uuid())
    email = db.Column(db.VARCHAR, unique=True)

    account = db.relationship(
        "Account", back_populates="user", cascade="all, delete")
