import pytest
import requests_mock

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
def test_login_with_valid_credentials(client):
        data = {
            "email": "tmm259@psu.edu",
            "password": "temp123",
        }
        response = client.post("/", data=data)
        assert response.status_code == 200




#Unit test 2 Test invalid login
def test_login_with_invalid_credentials(client):
    data = {
        "email": "tmm259@psu.edu",
        "password": "WrongPW",
    }
    response = client.post("/", data=data)
    response_data = response.get_data(as_text=True)
    assert "Incorrect Password please try again." in response_data

#System test 1:  Test that pages advance after successful login
def test_no_account(client):
    data = {
        "email": "anotherEmail@psu.edu",
        "password": "doesntmatter",
    }
    response = client.post("/", data=data)
    response_data = response.get_data(as_text=True)
    assert "User not found, please create an account" in response_data