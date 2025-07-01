from app.config.db import db, get_uuid


class Account(db.Model):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.UUID, primary_key=True, unique=True, default=get_uuid())
    username = db.Column(db.VARCHAR, unique=True)
    user_id = db.Column(db.UUID, db.ForeignKey(
        "auth.users.id"), nullable=False)

    user = db.relationship(
        "User", back_populates="account", cascade="all, delete")

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "user_id": self.user_id
        }
