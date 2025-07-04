import pytest
import csv
from app.utils.csv_reader_writer import fetch_updated_student_instance
import random
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

# #Unit Test 1: Search results are returned when valid student ID is entered
def test_search_for_student():
    testing_csv = ('data/updated_schoolmint.csv')
    ids = []

    if(testing_csv):
        with open(testing_csv, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                id = row[header.index('id')]
                ids.append(id)
    random_value = random.choice(ids)
    assert fetch_updated_student_instance(random_value) != 0
    assert fetch_updated_student_instance('$') == 0
    assert fetch_updated_student_instance(' 87') == 0
    assert fetch_updated_student_instance(' ') == 0
    assert fetch_updated_student_instance('2/2') == 0
    assert fetch_updated_student_instance('a') == 0


def test_student_search_no_param(client):
    response = client.get("/student_details/")
    assert response.status_code == 200
    assert b"No records for student" in response.data

def test_student_search_invalid_id(client):
    response = client.get("/student_details/?id_query=NOT_A_REAL_ID")
    print(response)
    assert response.status_code == 200
    assert b"No records for student" in response.data



        
