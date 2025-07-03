import pytest
from app.services.auth import validate_user_credentials
from app.services.auth import decode_token
from app.utils.jwt import generate_verify_token
from app.utils.exceptions import AppError


class TestValidateUserCredentials():
    def test_success(self):
        result = validate_user_credentials("example@gmail.com", "password")
        assert result is True

    def test_no_email(self):
        with pytest.raises(AppError) as exc:
            validate_user_credentials("", "password")
        assert str(exc.value) == "Email not provided"

    def test_no_password(self):
        with pytest.raises(AppError) as exc:
            validate_user_credentials("example@gmail.com", "")
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
