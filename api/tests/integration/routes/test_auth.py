from flask.testing import FlaskClient
from app.models.user import User
from app.models.account import Account
from app.config.db import db


class TestSignup:
    def remove_account(self, client: FlaskClient, email, username):
        # ensures that this account does not already exist
        old_account = Account.query.filter_by(username=username).first()
        if (old_account):
            db.session.delete(old_account)
            db.session.commit()

    def test_success(self, client: FlaskClient):
        email = "example1@gmail.com"
        username = "example1"
        self.remove_account(client, email, username)

        res = client.post("/auth/signup", data={
            "username": username,
            "email": email,
            "password": "passwordStrong1234!",
        })

        assert res.status_code == 200, "Signup failed"
        assert "verify_token" in res.json, "verify_token is not provided"

        user = User.query.filter_by(id=res.json["account"]["user_id"]).first()
        assert user, "User does not exist in supabase"
        assert user.email == email, "User's email does not match up"

        account = Account.query.filter_by(id=res.json["account"]["id"]).first()
        assert account, "Account does not exist in supabase"

        self.remove_account(client, email, username)

    def test_invalid_input(self, client: FlaskClient):
        email = ""
        username = "example1"
        self.remove_account(client, email, username)

        res = client.post("/auth/signup", data={
            "username": username,
            "email": email,
            "password": "passwordStrong1234!",
        })

        assert res.status_code == 400, "Request should have failed"
        assert "error" in res.json, "No error message returned"
        assert res.json["error"] == "Email not provided", "Incorrect error message"

        self.remove_account(client, email, username)

    def test_account_exists(self, client: FlaskClient):
        email = "example1@gmail.com"
        username = "example1"
        self.remove_account(client, email, username)

        res1 = client.post("/auth/signup", data={
            "username": username,
            "email": email,
            "password": "passwordStrong1234!",
        })

        assert res1.status_code == 200, "Signup failed"

        res2 = client.post("/auth/signup", data={
            "username": username,
            "email": email,
            "password": "passwordStrong1234!",
        })

        assert "error" in res2.json, "Error was not returned"
        assert res2.json["error"] == "Account already exists", "Error message not returned"
        assert res2.status_code != 200, "Account was created twice"
        assert res2.status_code == 409, "Status code should be 409"

        self.remove_account(client, email, username)


class TestLogin:
    def remove_account(self, client: FlaskClient, username):
        # ensures that this account does not already exist
        old_account = Account.query.filter_by(username=username).first()
        if (old_account):
            db.session.delete(old_account)
            db.session.commit()

    def create_account(self, client, username, email, password):
        self.remove_account(client, username)

        res1 = client.post("/auth/signup", data={
            "username": username,
            "email": email,
            "password": "password",
        })

        assert res1.status_code == 200, "Signup failed"
