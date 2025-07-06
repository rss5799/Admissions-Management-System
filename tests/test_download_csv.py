import csv
import pytest
from app import create_app
import shutil
import os

@pytest.fixture
def client():
    # Always reset updated_schoolmint.csv to known dummy data before the test
    shutil.copyfile(
        "data/DummyDataComplete.csv",
        "data/updated_schoolmint.csv"
    )

    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.mark.unit
def test_file_download(client):
    """
    This test ensures that the export_csv route correctly exports the contents
    of updated_schoolmint.csv. We'll load DummyDataComplete.csv into updated_schoolmint.csv,
    then request the export and check the response.
    """

    # Call the export route (must match your route method)
    response = client.get("/export_csv")
    assert response.status_code == 200

    # Get exported CSV contents
    downloaded_data = response.get_data(as_text=True)

    # Load DummyDataComplete header to compare
    with open("data/DummyDataComplete.csv", newline='') as f:
        reader = csv.reader(f)
        header_row = next(reader)

    # Check that each header field is present in exported CSV
    for field in header_row:
        assert field in downloaded_data
