from app.utils.exceptions import AppError
from app.utils.constants import FRONTEND_URL
from app.utils.jwt import decode_verify_token
import json


def validate_user_credentials(email, password):
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


def oauth_to_frontend(access_token):
    return f"""
        <html>
          <body>
            <script>
              window.opener.postMessage({json.dumps({
        "type": "OAUTH_SUCCESS",
                "data": {"access_token": access_token}
    })}, "{FRONTEND_URL}");
              window.close();
            </script>
            <p>Signing you in...</p>
          </body>
        </html>

"""
