from flask import request, g, jsonify, redirect, url_for, session
from functools import wraps
from supabase.client import AuthApiError
from app.utils.exceptions import AppError
from app.config.supabase import supabase
from app.models.account import Account
import logging

logger = logging.getLogger(__name__)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")
        token = header.split(" ")[1]

        if not token:
            raise AppError("No token provided", 401)

        try:
            response = supabase.auth.get_user(token)
        except AuthApiError:
            return redirect(url_for("routes.auth.refresh_tokens"))

        user_id = response.user.id
        account = Account.query.filter_by(user_id=user_id).first()
        if not account:
            raise AppError("Account could not be found", 401)

        return f(account, *args, **kwargs)

    return wrapper
