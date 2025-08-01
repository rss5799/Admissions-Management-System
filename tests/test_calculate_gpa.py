import pytest
from app import create_app
from app.services.matrix_calculator import calculate_gpa
import csv

expected_value = 3.2

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

#Unit test 8: Test GPA logic valid inputs
def test_calculate_gpa_logic():
    grades = {
        "english": "A",
        "math": "B",
        "science": "C",
        "social_studies": "B",
        "language": "A"
    }
    result = calculate_gpa(grades)
    assert result == expected_value

#Unit test 9:  Test GPA logic invalid inputs
def test_calculate_gpa_invalid():
    grades = {
        "english": "1",
        "math": "2",
        "science": "3",
        "social_studies": "4",
        "language": "5"
    }
    result = calculate_gpa(grades)
    assert result == 0.0

#System test 5: test empty data set advances to GPA page
def test_calculate_gpa_post_missing_fields(client):
    csv_file = "data/updated_schoolmint.csv"

    # Write dummy student row
    dummy_row = [
        "1", "Joe", "Smith", "9", "Other",
        "0", "0", "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0", "0", "0",
        "0", "0", "0"
    ]

    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(dummy_row)

    # Set session
    with client.session_transaction() as sess:
        sess["current_id"] = "1"

    data = {
        'english': '',
        'math': '',
        'science': '',
        'social_studies': '',
        'language': ''
    }

    response = client.post("/enter_report_card/", data=data)
    assert response.status_code == 200
    assert b"GPA" in response.data

#Unit test 10:  test no classes results in a gpa of 0
def test_calculate_gpa_no_classes():
    grades = {}
    result = calculate_gpa(grades)
    assert result == 0
