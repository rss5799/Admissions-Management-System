import pytest
from app import create_app
from app.services.matrix_calculator import calculate_gpa

expected_value = 3.2

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

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

def test_calculate_gpa_post_missing_fields(client):
    data = {
        'english': '',
        'math': '',
        'science': '',
        'social_studies': '',
        'language': ''
    }
    response = client.post("/calculate_gpa", data=data)
    assert response.status_code == 200
    assert b"GPA" in response.data

def test_calculate_gpa_no_classes():
    grades = {}
    result = calculate_gpa(grades)
    assert result == 0
