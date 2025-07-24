#I don't think we need anything here anymore but I didn't want to delete it in case we had to come back to it later for some reason
# config = {
#     'apiKey': "AIzaSyDObAkxu03wa769hSlSaYkGb27Z1SJ95Fg",
#     'authDomain': "admissionsmanagementsystem.firebaseapp.com",
#     'projectId': "admissionsmanagementsystem",
#     'storageBucket': "admissionsmanagementsystem.firebasestorage.app",
#     'messagingSenderId': "178704031743",
#     'appId': "1:178704031743:web:f0773e4dfa6702049711ca",
#     'databaseURL' : '' 
# }


# FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyDObAkxu03wa769hSlSaYkGb27Z1SJ95Fg")  

# FIREBASE_SIGN_IN_URL = (
#     f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
# )

# _session = {}

# def login_user(email, password):
#     response = requests.post(
#         FIREBASE_SIGN_IN_URL,
#         json={
#             "email": email,
#             "password": password,
#             "returnSecureToken": True
#         }
#     )

#     data = response.json()
#     print("FIREBASE RESPONSE:", data) 

#     if "idToken" in data:
#         _session["user"] = {
#             "email": data["email"],
#             "idToken": data["idToken"],
#             "refreshToken": data["refreshToken"]
#         }
#         return {"success": True, "token": data["idToken"], "user": {"email": data["email"]}}
#     else:
#         return {"success": False, "error": data.get("error", {})}


# def get_current_user():
#     return _session.get("user", None)


# def logout_user():
#     _session.clear()
