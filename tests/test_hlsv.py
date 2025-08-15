import pytest
import csv
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

# UT-19
def test_high_level_student_view_visibility(client):
    # Load student IDs from CSV
    csv_path = 'data/updated_schoolmint.csv'
    ids = []
    expected_headers = [
    'id', 'lname', 'fname', 'grade', 'current_school', 'status',
       'test_date_sign_up','Predicted Unweighted GPA'
    ]
    
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        header_row = next(reader)
        for row in reader:
            if row and row[0].strip(): 
                ids.append(row[header_row.index("id")])

    assert len(ids) > 0, "No student IDs found in CSV"

    # Access hlsv page...maybe we should rename the route?
    response = client.get('/point_inputs/')
    assert response.status_code == 200

    # Confirm student IDs are visible in response
    for student_id in ids:
        assert bytes(student_id.strip(), 'utf-8') in response.data

    # Confirm all expected headers are present
    for header in expected_headers:
        assert bytes(header, 'utf-8') in response.data

    # Post-condition: navigating away still works 
    menu_response = client.get('/menu')
    assert menu_response.status_code == 200 or menu_response.status_code == 302

# UT-20
def test_redirect_from_hlsv_to_student_details(client):
    # Load a real student ID
    csv_path = 'data/updated_schoolmint.csv'
    student_ids = []

    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row and row[0].strip():
                student_ids.append(row[header.index("id")])

    assert student_ids, "No student IDs found in CSV"
    test_id = student_ids[0]

    # Go to hlsv
    response_hlsv = client.get('/point_inputs/')
    assert response_hlsv.status_code == 200
    assert bytes(test_id, 'utf-8') in response_hlsv.data

    # Select a student ID to view details
    response_detail = client.get(f'/student_details/?id_query={test_id}')
    assert response_detail.status_code == 200
    assert b"Student Details" in response_detail.data
    assert bytes(test_id, 'utf-8') in response_detail.data

    # Navigate back to high-level view
    response_back = client.get('/point_inputs/')
    assert response_back.status_code == 200
    assert bytes(test_id, 'utf-8') in response_back.data

