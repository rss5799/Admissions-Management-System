# import pytest
# from app.auth_controller import login_user, get_current_user, logout_user

import pytest
import pyrebase


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


def test_login_with_valid_credentials():
    user = auth.sign_in_with_email_and_password(VALID_EMAIL, VALID_PASSWORD)
    assert user['email'] == VALID_EMAIL

#TODO add a test for invalid login



    


# def test_login_with_invalid_credentials():
#     logout_user()
#     result = login_user(VALID_EMAIL, INVALID_PASSWORD)
    
#     assert result["success"] is False
#     assert "error" in result


# def test_session_persistence():
#     logout_user()
#     login_user(VALID_EMAIL, VALID_PASSWORD)

#     # Simulate a "page refresh"
#     user = get_current_user()

#     assert user is not None
#     assert user["email"] == VALID_EMAIL
