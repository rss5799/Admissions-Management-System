import pytest
import csv
from app.utils.csv_reader_writer import fetch_updated_student_instance
import random
from app import create_app
import app.utils.helpers as h

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


#Unit Test 6:  Ensure updated student instance is fetched when input is valid
@pytest.mark.unit
def test_search_for_student():
    """
    Unit Test 6:
    Ensure updated student instance is fetched correctly for valid and invalid IDs.
    """
    # Write known dummy data first
    h.write_dummy_schoolmint_csv()

    # Collect IDs from dummy data
    ids = []
    with open('data/updated_schoolmint.csv', 'r') as file:
        header = next(file).strip().split(",")
        id_idx = header.index("id")
        for line in file:
            row = line.strip().split(",")
            if row and row[id_idx]:
                ids.append(row[id_idx])

    # Pick a random valid ID from dummy data
    random_value = random.choice(ids)
    assert fetch_updated_student_instance(random_value) != 0

    # Check various invalid IDs return 0
    assert fetch_updated_student_instance('$') == 0
    assert fetch_updated_student_instance('87') == 0
    assert fetch_updated_student_instance(' ') == 0
    assert fetch_updated_student_instance('2/2') == 0
    assert fetch_updated_student_instance('a') == 0


#Unit test 3: Assert empty input returns a "no records" result
def test_student_search_no_param(client):
    response = client.get("/student_details/")
    assert response.status_code == 200
    assert b"No records for student" in response.data

#Unit test 4:  Assert invalid input returns a "no records" result
def test_student_search_invalid_id(client):
    response = client.get("/student_details/?id_query=NOT_A_REAL_ID")
    assert response.status_code == 200
    assert b"No records for student" in response.data


#System test 2: Ensure student details load when valid ID is queried
def test_student_search_valid_id(client):
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
    assert b"Student Details" in response.data

    # Clean up
    with open(csv_file, "r") as f:
        rows = list(csv.reader(f))
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            if row[0] != "1":
                writer.writerow(row)






        
