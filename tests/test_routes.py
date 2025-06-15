import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_unresponsive_students(client):
    response = client.get("/unresponsive_students/")
    assert response.status_code == 200
    assert b"Unresponsive Students" in response.data

def test_calculate_gpa_post(client):
    data = {
        'english': '90',
        'math': '85',
        'science': '95',
        'social_studies': '88',
        'language': '92'
    }
    response = client.post("/calculate_gpa", data=data)
    assert response.status_code == 200
    assert b"GPA" in response.data

def test_student_search(client):
    response = client.get("/student_details/?id_query=12345")
    assert response.status_code == 200
    assert b"student_details" in response.data

def test_route_not_found(client):
    response = client.get("/this_route_does_not_exist")
    assert response.status_code == 404

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_profile_route(client):
    response = client.get("/profile/12345")
    assert response.status_code == 404

