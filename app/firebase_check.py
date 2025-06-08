import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import pandas as pd

# Use the relative path to the credentials file
key_path = os.path.join(os.path.dirname(__file__), "/Users/taracan/Documents/SWENG894/Admissions-Management-System/app/credentials/firebase_key.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()

# Firestore test
print("Fetching students...")
students_ref = db.collection("students")
docs = students_ref.stream()

empty = True
for doc in docs:
    empty = False
    print(f"Found student: {doc.id} → {doc.to_dict()}")

if empty:
    print("No students found in database.")

# Firebase Auth test
print("\nFetching first 10 users from Firebase Auth...")
page = auth.list_users(max_results=10)
for user in page.users:
    print(f"User: {user.uid} | Email: {user.email}")


print("\nFirebase connection successful.")

def upload_csv_to_firestore():
    try:
        df = pd.read_csv("/Users/taracan/Documents/SWENG894/Admissions-Management-System/DummyData.csv")
    except FileNotFoundError:
        print(f"Error:CSV file not found at {csv_file_path}")
        return
    for index, row in df.iterrows():
        doc_ref = db.collection("student_rc_and_test_scores").document()
        doc_ref.set(row.to_dict())
    print("Data uploaded successfully!")

upload_csv_to_firestore()