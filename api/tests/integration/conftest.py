import pytest
from app import create_app
from app.config.db import db


@pytest.fixture
def client():
    app = create_app()

    with app.app_context():
        yield app.test_client()
