import jwt
from datetime import datetime, timedelta
from app.utils.constants import SECRET_KEY


def generate_verify_token(email, expiry=300):
    exp = datetime.utcnow() + timedelta(seconds=expiry)
    payload = {"email": email, "exp": exp}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_verify_token(token):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return decoded
