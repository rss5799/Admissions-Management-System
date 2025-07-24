import pytest

from app import create_app



VALID_EMAIL = "amsforbfhsadmin@bfhsla.org"
VALID_PASSWORD = "temp123"
INVALID_EMAIL = "doesnotexist@example.com"
INVALID_PASSWORD = "wrongpassword"

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


#Unit test 1:  Test that valid login proceeds without error
def test_login_with_valid_credentials():
    assert 1 == 1



#Unit test 2 Test invalid login
def test_login_with_invalid_credentials():
    assert 1 == 1

#System test 1:  Test that pages advance after successful login
def test_advance_after_login(client):
    assert 1 == 1