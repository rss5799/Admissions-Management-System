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

def test_firebase_initialization(firestore_client):
    assert firestore_client is not None

def test_read_sample_data(firestore_client):
    docs = firestore_client.collection("students").stream()
    doc_list = list(docs)
    assert len(doc_list) > 0 

def test_write_student_record(firestore_client):
    test_doc = {
        "name": "Test Student",
        "gpa": 3.8,
        "status": "testing"
    }
    doc_ref = firestore_client.collection("students").document("test-student")
    doc_ref.set(test_doc)
    fetched = doc_ref.get().to_dict()
    assert fetched["name"] == "Test Student"
