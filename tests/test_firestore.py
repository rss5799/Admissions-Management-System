import pytest
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Loads the credentials if they don't already exist
@pytest.fixture(scope="module")
def firestore_client():
    if not firebase_admin._apps:
        cred = credentials.Certificate("credentials/firebase_key.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()

def test_read_sample_data(firestore_client):
    # Arrange: Write a test doc
    test_doc = {
        "name": "Read Test Student",
        "gpa": 3.6,
        "status": "read_test"
    }
    doc_ref = firestore_client.collection("students").document("test-read-student")
    doc_ref.set(test_doc)

    # Read it back
    fetched = doc_ref.get().to_dict()

    # Check if the data matches
    assert fetched["name"] == "Read Test Student"
    assert fetched["gpa"] == 3.6
    doc_ref.delete()
