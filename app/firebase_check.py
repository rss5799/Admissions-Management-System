import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import pandas as pd

# Use the relative path to the credentials file
key_path = os.path.join(os.path.dirname(__file__), "/Users/taracan/Documents/SWENG894/Admissions-Management-System/credentials/firebase_key.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

# Access Firestore
db = firestore.client()


def upload_csv_to_firestore():
    try:
        df = pd.read_csv("/Users/taracan/Documents/SWENG894/Admissions-Management-System/DummyDataLite.csv")
    except FileNotFoundError:
        print(f"Error:CSV file not found at {csv_file_path}")
        return
    for index, row in df.iterrows():
        doc_ref = db.collection("studentObject").document()
        doc_ref.set(row.to_dict())
    print("Data uploaded successfully!")

upload_csv_to_firestore()