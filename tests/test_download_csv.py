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

#System test 6:  Test exports page renders
@pytest.mark.unit
def test_exports_page(client):
    response = client.get("/exports/")
    assert response.status_code == 200

#System test 7:  Test all headers persist to downloaded csv
@pytest.mark.unit
def test_file_download(client):
    if os.path.exists('data/updated_schoolmint.csv'):
        testing_data = ('data/updated_schoolmint.csv')
        response = client.post("/export_csv")
        assert response.status_code == 200
        
        downloaded_data = response.get_data(as_text=True)

        with open(testing_data, 'r') as firstfile:
            reader = csv.reader(firstfile)
            headerOriginal = next(reader)

    
        for item in headerOriginal:
            assert item in downloaded_data


#System test 8:  Ensure export_csv page renders
@pytest.mark.unit
def test_file_upload_input_present(client):
    response = client.post("/export_csv")
    assert response.status_code == 200
