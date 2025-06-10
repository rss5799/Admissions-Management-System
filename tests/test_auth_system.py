import pytest
from app.auth_controller import login_user, get_current_user, logout_user

VALID_EMAIL = "jr_scott25@yahoo.com"         
VALID_PASSWORD = "chaP1stick!!"           
INVALID_EMAIL = "doesnotexist@example.com"
INVALID_PASSWORD = "wrongpassword"

def test_login_with_valid_credentials():
    logout_user()
    result = login_user(VALID_EMAIL, VALID_PASSWORD)
    
    assert result["success"] is True
    assert "token" in result
    assert result["user"]["email"] == VALID_EMAIL


def test_login_with_invalid_credentials():
    logout_user()
    result = login_user(VALID_EMAIL, INVALID_PASSWORD)
    
    assert result["success"] is False
    assert "error" in result


def test_session_persistence():
    logout_user()
    login_user(VALID_EMAIL, VALID_PASSWORD)

    # Simulate a "page refresh"
    user = get_current_user()

    assert user is not None
    assert user["email"] == VALID_EMAIL
