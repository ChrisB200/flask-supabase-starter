from flask import Blueprint, jsonify, request, session
from supabase.client import AuthApiError
from app.utils.exceptions import AppError
from app.utils.jwt import generate_verify_token
from app.utils.decorators import login_required
from app.config.supabase import supabase
from app.config.db import db
from app.models.account import Account
from app.services.auth import validate_user_signup
from app.services.auth import validate_user_login
from app.services.auth import decode_token
import logging

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    validate_user_signup(username, email, password)

    account = Account.query.filter_by(username=username).first()

    if account:
        raise AppError("Account already exists", 409)

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        account = Account(username=username, user_id=response.user.id)
        db.session.add(account)
        db.session.commit()

        verify_token = generate_verify_token(email)

        return jsonify(verify_token=verify_token, account=account.to_json()), 200
    except AuthApiError as e:
        db.session.rollback()
        raise AppError(e.message)
    except Exception as e:
        db.session.rollback()
        raise e


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    validate_user_login(email, password)

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })

        access_token = response.session.access_token
        refresh_token = response.session.refresh_token

        session["refresh_token"] = refresh_token

        return jsonify(access_token=access_token)
    except AuthApiError as e:
        if e.message == "Email not confirmed":
            verify_token = generate_verify_token(email)
            return jsonify(verify_token=verify_token), 200

        raise AppError(e.message, 401)


@auth_bp.route("/code/verify", methods=["POST"])
def verify_code():
    code = request.form.get("code")

    token = request.headers.get("Authorization")
    data = decode_token(token)

    response = supabase.auth.verify_otp({
        "email": data["email"],
        "token": code,
        "type": "email"
    })

    access_token = response.session.access_token
    refresh_token = response.session.refresh_token
    session["refresh_token"] = refresh_token

    return jsonify(access_token=access_token)


@auth_bp.route("/code/resend", methods=["POST"])
def resend_code():
    email = request.form.get("email")

    supabase.auth.resend({
        "type": "signup",
        "email": email,
    })

    return jsonify("Code has been resent"), 200


@auth_bp.route("/refresh", methods=["GET"])
def refresh_tokens():
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        raise AppError("No refresh token", 401)

    try:
        response = supabase.auth.refresh_session(refresh_token)
    except AuthApiError as e:
        if e.message == "Invalid Refresh Token: Refresh Token Not Found":
            raise AppError("No refresh token", 401)

    access_token = response.session.access_token
    refresh_token = response.session.refresh_token
    session["refresh_token"] = refresh_token

    return jsonify(access_token=access_token)


@auth_bp.route("/authenticated", methods=["GET"])
@login_required
def authenticated(current_user):
    return jsonify(current_user.to_json())
