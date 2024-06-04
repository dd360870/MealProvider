# tests/conftest.py
import pytest
from flaskr import create_app
from flaskr.db import db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': ':memory:',
    })

    with app.app_context():
        # db.create_all()
        yield app

    # with app.app_context():
    #     db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
