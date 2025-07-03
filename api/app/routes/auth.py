from flask import Blueprint, jsonify, request, session, url_for, redirect
from supabase.client import AuthApiError
from app.utils.exceptions import AppError
from app.utils.jwt import generate_verify_token
from app.utils.decorators import login_required
from app.utils.constants import FRONTEND_URL
from app.config.supabase import supabase
from app.config.supabase import supabase_dev
from app.config.db import db
from app.models.account import Account
from app.models.user import User
from app.services.auth import validate_user_credentials
from app.services.auth import decode_token
from app.services.auth import oauth_to_frontend
import logging
from jwt.exceptions import ExpiredSignatureError

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    password = request.form.get("password")

    validate_user_credentials(email, password)

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
    except AuthApiError as e:
        db.session.rollback()
        raise AppError(e.message)

    try:
        account = Account(user_id=response.user.id)
        db.session.add(account)
        db.session.commit()

        verify_token = generate_verify_token(email)

        return jsonify(verify_token=verify_token, account=account.to_json()), 200
    except Exception as e:
        db.session.rollback()
        user = User.query.filter_by(id=response.user.id)
        if (user):
            return db.session.delete(user)
            db.session.commit()
        raise e


@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    validate_user_credentials(email, password)

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

    try:
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
    except AuthApiError as e:
        raise AppError(e.message, 400)
    except ExpiredSignatureError:
        raise AppError("Verify expired", 400)


@auth_bp.route("/code/resend", methods=["GET"])
def resend_code():
    token = request.headers.get("Authorization")

    try:
        data = decode_token(token)
        supabase.auth.resend({
            "type": "signup",
            "email": data["email"],
        })

        return jsonify(message="Code has been resent"), 200
    except AuthApiError as e:
        raise AppError(e.message, 400)
    except ExpiredSignatureError:
        raise AppError("Verification expired", 400)


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


@auth_bp.route("/google")
def auth_google():
    print(url_for("routes.auth.auth_callback", _external=True))
    res = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {"redirect_to": url_for("routes.auth.auth_callback", _external=True)}
    })
    return jsonify(url=res.url)


@auth_bp.route("/callback")
def auth_callback():
    code = request.args.get("code")
    if not code:
        raise AppError("No auth code")

    try:
        response = supabase.auth.exchange_code_for_session({"auth_code": code})
    except AuthApiError as e:
        if e.message == "Invalid Refresh Token: Refresh Token Not Found":
            raise AppError("No refresh token", 401)

    account = Account.query.filter_by(user_id=response.user.id).first()
    if not account:
        account = Account(user_id=response.user.id)
        db.session.add(account)
        db.session.commit()

    access_token = response.session.access_token
    refresh_token = response.session.refresh_token
    session["refresh_token"] = refresh_token

    return oauth_to_frontend(access_token)


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    email = request.form.get("email")

    if not email:
        raise AppError("No email was provided")

    try:
        supabase.auth.reset_password_for_email(
            email, {"redirect_to": f"{FRONTEND_URL}/reset-password"})
    except AuthApiError as e:
        raise AppError(e.message)

    return jsonify(message="reset email sent")


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    password = request.form.get("password")
    access_token = request.form.get("access_token")
    refresh_token = request.form.get("refresh_token")

    if not password:
        raise AppError("No password was provided")
    if not access_token:
        raise AppError("No access token was provided")
    if not refresh_token:
        raise AppError("No refresh token was provided")

    try:
        supabase_dev.auth.set_session(access_token, refresh_token)

        supabase_dev.auth.update_user({"password": password})
    except AuthApiError as e:
        raise AppError(e.message)

    return jsonify(message="success")
