import pytest
import csv
from app.utils.csv_reader_writer import fetch_updated_student_instance
import random
from app import create_app

TEST_ID = "999999"
TEST_FIRST = "Testy"
TEST_LAST = "McTestface"

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


#Unit Test 6:  Ensure updated student instance is fetched when input is valud
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

#Unit test 3: Assert empty input returns a "no records" result
def test_student_search_no_param(client):
    response = client.get("/student_details/")
    assert response.status_code == 302


#Unit test 4:  Assert invalid input returns a "no records" result
def test_student_search_invalid_id(client):
    response = client.get("/student_details/?id_query=NOT_A_REAL_ID")
    assert response.status_code == 302


#System test 2: Ensure student details load when valid ID is queried
def test_student_search_valid_id(client):
    testing_csv = ('data/updated_schoolmint.csv')
    ids = []
    print(ids)

    if(testing_csv):
        with open(testing_csv, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                id = row[header.index('id')]
                if(id != ''):
                    ids.append(id)
        random_value = random.choice(ids)
        id_to_test = random_value
        response = client.get(f"/student_details/?id_query={id_to_test}")
        assert b"Student Details" in response.data

def get_first_student():
    """
    Fetches first student from CSV file to use in tests.
    """
    csv_file = "../data/DummyDataComplete.csv"
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["id"]:
                return row["id"], row["first"], row["last"]
    raise ValueError("No student found in test CSV!")

def test_student_details_page_loads(client):
    student_id, first, last = get_first_student()

    with client.session_transaction() as sess:
        sess["current_id"] = student_id

    response = client.get(
        f"/student_details/?id_query={student_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Student Data" in response.data

def test_student_details_table_headers(client):
    student_id, first, last = get_first_student()

    with client.session_transaction() as sess:
        sess["current_id"] = student_id

    response = client.get(
        f"/student_details/?id_query={student_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    for header in [b"id", b"first", b"last"]:
        assert header in response.data

def test_student_details_shows_data(client):
    student_id, first, last = get_first_student()

    with client.session_transaction() as sess:
        sess["current_id"] = student_id

    response = client.get(
        f"/student_details/?id_query={student_id}",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert student_id.encode() in response.data
    assert first.encode() in response.data
    assert last.encode() in response.data
    assert b'<a href=' in response.data








        
