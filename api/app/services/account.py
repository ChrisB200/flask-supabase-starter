from app.models.account import Account
import random
import string


def generate_random_username(base: str, length: int = 3) -> str:
    """Generate a random username by appending a random string to the base."""
    random_suffix = ''.join(random.choices(string.digits, k=length))
    return f"{base.lower()}{random_suffix}"


def is_username_exist(username):
    account = Account.query.filter_by(username=username).first()
    if account:
        return True
    return False


def generate_unique_username(email):
    email = email.split("@")
    base = email[0]
    if "." in base:
        base = base.split(".")[0]

    while True:
        username = generate_random_username(base)
        if not (is_username_exist(username)):
            return username
