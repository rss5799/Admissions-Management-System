import requests
import os

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "your-api-key-here")  # replace or load via env

FIREBASE_SIGN_IN_URL = (
    f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
)

# Optional: simulate user session persistence
_session = {}

def login_user(email, password):
    response = requests.post(
        FIREBASE_SIGN_IN_URL,
        json={
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
    )

    data = response.json()

    if "idToken" in data:
        _session["user"] = {
            "email": data["email"],
            "idToken": data["idToken"],
            "refreshToken": data["refreshToken"]
        }
        return {"success": True, "token": data["idToken"], "user": {"email": data["email"]}}
    else:
        return {"success": False, "error": data.get("error", {})}


def get_current_user():
    return _session.get("user", None)


def logout_user():
    _session.clear()
