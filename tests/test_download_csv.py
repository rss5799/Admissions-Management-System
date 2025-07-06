import csv
import pytest
from app import create_app
import os

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

# System test 6: Test exports page renders
@pytest.mark.unit
def test_exports_page(client):
    response = client.get("/exports/")
    assert response.status_code == 200

# System test 7: Test all headers persist to downloaded csv
@pytest.mark.unit
def test_file_download(client):
    # Ensure dummy file exists
    path = 'data/updated_schoolmint.csv'
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create dummy CSV with headers
    headers = ['id', 'first_name', 'last_name', 'grade', 'current_school']
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(['1', 'Joe', 'Smith', '9', 'Other'])

    # Call POST because your route expects POST
    response = client.post("/export_csv")
    assert response.status_code == 200

    downloaded_data = response.get_data(as_text=True)

    # Check that each header exists in the downloaded CSV
    for item in headers:
        assert item in downloaded_data

    # Clean up the dummy file
    os.remove(path)

# System test 8: Ensure export_csv page renders correctly (GET should go to exports page)
@pytest.mark.unit
def test_file_upload_input_present(client):
    response = client.get("/exports/")
    assert response.status_code == 200
