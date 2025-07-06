import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


#System test 25:  Test unresponsive students route
def test_unresponsive_students(client):
    response = client.get("/unresponsive_students/")
    assert response.status_code == 200
    assert b"Unresponsive Students" in response.data


#System test 26:  Test enter report card route
def test_calculate_gpa_post(client):
    data = {
        'english': '90',
        'math': '85',
        'science': '95',
        'social_studies': '88',
        'language': '92'
    }
    response = client.post("/enter_report_card/", data=data)
    assert response.status_code == 200
    assert b"GPA" in response.data


#System test 27:  Test student details route (invalid query)
def test_student_search(client):
    response = client.get("/student_details/?id_query=12345")
    assert response.status_code == 200
    assert b"No records for student" in response.data


#System test 28:  Test invalid route
def test_route_not_found(client):
    response = client.get("/this_route_does_not_exist")
    assert response.status_code == 404


#System test 29:  Test home route
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


#System test 30:  Test invalid route
def test_profile_route(client):
    response = client.get("/profile/12345")
    assert response.status_code == 404


#System test 31: Test home route
def test_home_route(client):
    response = client.post("/")
    assert response.status_code == 200


#System test 32:  Test enter report card route
def test_enter_report_card_route(client):
    response = client.get("/enter_report_card/")
    assert response.status_code == 200

    response = client.post("enter_report_card/")
    response_data = response.get_data(as_text=True)
    assert f"Return to Student Scores" in response_data

