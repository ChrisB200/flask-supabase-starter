from flask import Blueprint, jsonify, request
from app.utils.decorators import login_required
from app.utils.exceptions import AppError
from app.models.account import Account
from app.config.db import db
import logging

account_bp = Blueprint("account", __name__)
logger = logging.getLogger(__name__)


@account_bp.route("/name", methods=["POST"])
@login_required
def update_name(current_account: Account):
    name = request.form.get("name")

    if not name:
        raise AppError("name is required")

    if len(name) < 4 or len(name) > 16:
        raise AppError("name must be between 4 and 16 characters")

    current_account.name = name

    db.session.add(current_account)
    db.session.commit()

    return jsonify(message="succesfully updated name")
