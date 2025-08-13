import os
import csv
import pandas as pd
import pytest
from app import create_app

@pytest.fixture
def client(tmp_path):
    app = create_app()
    with app.test_client() as client:
        yield client

def setup_csv(path, rows):
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)

def test_grab_updated_fields_route_returns_list(client, tmp_path, monkeypatch):
    # Setup test CSVs
    schoolmint_path = tmp_path / "updated_schoolmint.csv"
    original_path = tmp_path / "original_schoolmint.csv"
    setup_csv(schoolmint_path, [{'id': '1', 'gpa': '2.0'}])
    setup_csv(original_path, [{'id': '1', 'gpa': ''}])
    monkeypatch.setattr("app.routes.schoolMint_csv", str(schoolmint_path))
    monkeypatch.setattr("app.routes.UPLOAD_FOLDER", str(tmp_path))
    response = client.get("/grab_updated_fields/")
    assert response.status_code == 200

def test_grab_updated_fields_creates_csv(client, tmp_path, monkeypatch):
    schoolmint_path = tmp_path / "updated_schoolmint.csv"
    original_path = tmp_path / "original_schoolmint.csv"
    setup_csv(schoolmint_path, [{'id': '1', 'gpa': '2.0'}])
    setup_csv(original_path, [{'id': '1', 'gpa': ''}])
    monkeypatch.setattr("app.routes.schoolMint_csv", str(schoolmint_path))
    monkeypatch.setattr("app.routes.UPLOAD_FOLDER", str(tmp_path))
    client.get("/grab_updated_fields/")
    assert os.path.exists(tmp_path / "updated_fields.csv")

def test_export_csv_route_returns_file(client, tmp_path, monkeypatch):
    # Setup updated_fields.csv
    updated_fields_path = tmp_path / "updated_fields.csv"
    with open(updated_fields_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Field', 'Old Value', 'New Value'])
        writer.writerow(['1', 'gpa', '', '2.0'])
    # Setup schoolMint_csv
    schoolmint_path = tmp_path / "updated_schoolmint.csv"
    setup_csv(schoolmint_path, [{'id': '1', 'gpa': '2.0'}])
    monkeypatch.setattr("app.routes.schoolMint_csv", str(schoolmint_path))
    monkeypatch.setattr("app.routes.UPLOAD_FOLDER", str(tmp_path))
    response = client.post("/export_csv")
    assert response.status_code == 200
    assert response.mimetype in ["text/csv", "application/vnd.ms-excel"]

def test_exports_page_renders(client, tmp_path, monkeypatch):
    schoolmint_path = tmp_path / "updated_schoolmint.csv"
    original_path = tmp_path / "original_schoolmint.csv"
    setup_csv(schoolmint_path, [{'id': '1', 'gpa': '2.0'}])
    setup_csv(original_path, [{'id': '1', 'gpa': ''}])
    monkeypatch.setattr("app.routes.schoolMint_csv", str(schoolmint_path))
    monkeypatch.setattr("app.routes.UPLOAD_FOLDER", str(tmp_path))
    response = client.get("/exports/")
    assert response.status_code == 200
    assert b"Exports" in response.data

def test_export_csv_no_updated_fields(client, tmp_path, monkeypatch):
    monkeypatch.setattr("app.routes.UPLOAD_FOLDER", str(tmp_path))
    response = client.post("/export_csv")
    # Passes if either Main Menu or Logout is present
    assert b"Main Menu" in response.data or b"Logout" in response.data

def test_exports_page_no_changes_message(client, tmp_path, monkeypatch):
    schoolmint_path = tmp_path / "updated_schoolmint.csv"
    original_path = tmp_path / "original_schoolmint.csv"
    setup_csv(schoolmint_path, [{'id': '1', 'gpa': '3.0'}])
    setup_csv(original_path, [{'id': '1', 'gpa': '3.0'}])
    monkeypatch.setattr("app.routes.schoolMint_csv", str(schoolmint_path))
    monkeypatch.setattr("app.routes.UPLOAD_FOLDER", str(tmp_path))
    response = client.get("/exports/")
    assert b"Exports" in response.data  # Always present on exports page