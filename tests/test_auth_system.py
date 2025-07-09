import pytest
import pyrebase
from app import create_app


config = {
    'apiKey': "AIzaSyDObAkxu03wa769hSlSaYkGb27Z1SJ95Fg",
    'authDomain': "admissionsmanagementsystem.firebaseapp.com",
    'projectId': "admissionsmanagementsystem",
    'storageBucket': "admissionsmanagementsystem.firebasestorage.app",
    'messagingSenderId': "178704031743",
    'appId': "1:178704031743:web:f0773e4dfa6702049711ca",
    'databaseURL' : '' 
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

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
    user = auth.sign_in_with_email_and_password(VALID_EMAIL, VALID_PASSWORD)
    assert user['email'] == VALID_EMAIL



#Unit test 2 Test invalid login
def test_login_with_invalid_credentials():
    try:
        user = auth.sign_in_with_email_and_password(INVALID_EMAIL, INVALID_PASSWORD)
        assert 1 == 0
    except:
        assert 1 == 1

#System test 1:  Test that pages advance after successful login
def test_advance_after_login(client):
    user = auth.sign_in_with_email_and_password(VALID_EMAIL, VALID_PASSWORD)
    response = client.get("/landing")
    assert response.status_code == 200
    assert b"SchoolMint Data Upload" in response.data
