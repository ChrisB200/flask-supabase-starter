from app.utils.exceptions import AppError
from app.utils.jwt import decode_verify_token


def validate_user_signup(username, email, password):
    if not username:
        raise AppError("Username not provided")

    if len(username) > 15 or len(username) < 4:
        raise AppError("Username must be between 4 and 15 characters")

    if not email:
        raise AppError("Email not provided")

    if not password:
        raise AppError("Password not provided")

    return True


def validate_user_login(email, password):
    if not email:
        raise AppError("Email not provided")

    if not password:
        raise AppError("Password not provided")

    return True


def decode_token(token):
    if not token:
        raise AppError("No verify token provided", 401)
    token = token.split(" ")[1]

    data = decode_verify_token(token)

    return data
