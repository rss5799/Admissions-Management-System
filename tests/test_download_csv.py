import csv
import pytest
from app import create_app
import shutil

@pytest.fixture
def client():
    # Always reset updated_schoolmint.csv to known dummy data before the test
    shutil.copyfile(
        "DummyDataComplete.csv",
        "updated_schoolmint.csv"
    )

    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.mark.unit
def test_file_download(client):
    # Use GET or POST depending on route definition
    response = client.get("/export_csv")
    assert response.status_code == 200

    downloaded_data = response.get_data(as_text=True)

    # Check exported CSV has all expected headers
    with open("DummyDataComplete.csv", newline='') as f:
        reader = csv.reader(f)
        header_row = next(reader)

    for field in header_row:
        assert field in downloaded_data
