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

@pytest.fixture
def insert_test_student():
    csv_file = "data/updated_schoolmint.csv"
    dummy_row = [
        TEST_ID, TEST_FIRST, TEST_LAST, "9", "Other",
        "0", "0", "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0", "0", "0",
        "0", "0", "0"
    ]

    exists = False
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == TEST_ID:
                exists = True
                break

    if not exists:
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(dummy_row)

def test_student_details_page_loads(client):
    with open("data/updated_schoolmint.csv", newline="") as f:
        reader = csv.DictReader(f)
        row = next(reader)
        id_to_test = row["id"]
        first_name = row["first_name"]
        last_name = row["last_name"]

    with client.session_transaction() as sess:
        sess["current_id"] = id_to_test

    response = client.get(
        f"/student_details/?id_query={id_to_test}",
        follow_redirects=True
    )
    print("Fetch result:", fetch_updated_student_instance(id_to_test))
    print("\n=== RESPONSE BODY ===\n", response.data.decode(errors="replace"))
    assert response.status_code == 200
    assert b"Student Data" in response.data
    assert first_name.encode() in response.data
    assert last_name.encode() in response.data







        
