import pytest
from app.services.auth import validate_user_signup
from app.services.auth import validate_user_login
from app.services.auth import decode_token
from app.utils.jwt import generate_verify_token
from app.utils.exceptions import AppError


class TestValidateUserSignup():
    def test_success(self):
        result = validate_user_signup(
            "example", "example@gmail.com", "password")
        assert result is True

    def test_no_username(self):
        with pytest.raises(AppError) as exc:
            validate_user_signup("", "example@gmail.com", "password")
        assert str(exc.value) == "Username not provided"

    def test_short_username(self):
        with pytest.raises(AppError) as exc:
            validate_user_signup("abc", "example@gmail.com", "password")
        assert str(exc.value) == "Username must be between 4 and 15 characters"

    def test_long_username(self):
        with pytest.raises(AppError) as exc:
            username = "abcdefghijklmnopqrstuv"
            validate_user_signup(username, "example@gmail.com", "password")
        assert str(exc.value) == "Username must be between 4 and 15 characters"

    def test_no_email(self):
        with pytest.raises(AppError) as exc:
            validate_user_signup("example", "", "password")
        assert str(exc.value) == "Email not provided"

    def test_no_password(self):
        with pytest.raises(AppError) as exc:
            validate_user_signup("example", "example@gmail.com", "")
        assert str(exc.value) == "Password not provided"


class TestValidateUserLogin():
    def test_success(self):
        result = validate_user_login("example@gmail.com", "password")
        assert result is True

    def test_no_email(self):
        with pytest.raises(AppError) as exc:
            validate_user_login("", "password")
        assert str(exc.value) == "Email not provided"

    def test_no_password(self):
        with pytest.raises(AppError) as exc:
            validate_user_login("example@gmail.com", "")
        assert str(exc.value) == "Password not provided"


class TestDecodeToken():
    def test_success(self):
        token = "Bearer " + generate_verify_token("example1@gmail.com")
        result = decode_token(token)
        assert result, "Token unable to be decoded"
        assert result["email"] == "example1@gmail.com", "Email does not match"

    def test_no_token(self):
        with pytest.raises(AppError) as exc:
            decode_token("")
        assert str(exc.value) == "No verify token provided", "Error is incorrect"
