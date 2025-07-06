import pytest
from app import create_app
import csv
import app.utils.helpers as h

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
    # Ensure dummy data is in place
    h.write_dummy_schoolmint_csv()

    with client.session_transaction() as sess:
        sess["current_id"] = "1"

    data = {
        'english': 'A',
        'math': 'B',
        'science': 'A',
        'social_studies': 'B',
        'language': 'A'
    }
    response = client.post("/enter_report_card/", data=data)
    assert response.status_code == 200
    assert b"GPA" in response.data


#System test 27:  Test student details route (invalid query)
def test_student_search(client):
    dummy_row = [
        "1", "Joe", "Smith", "9", "Other", "None", "None", "None", 
        "None", "None", "None", "None", "None", "None", "None", 
        "None", "None", "None", "None", "None", "None"
    ]
    csv_file = "data/updated_schoolmint.csv"

    # Write dummy student
    with open(csv_file, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(dummy_row)

    response = client.get("/student_details/?id_query=1")
    assert response.status_code == 200
    assert b"Student Details" in response.data

    # Clean up
    with open(csv_file, "r") as f:
        rows = list(csv.reader(f))
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            if row[0] != "1":
                writer.writerow(row)

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

