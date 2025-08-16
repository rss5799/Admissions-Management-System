import pytest
import csv
from app import create_app
import requests

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

#This tests that all IDs render
def test_sort_by_id_ascending(client):
    #get all the ids in the data
    testing_data = 'data/updated_schoolmint.csv'
    ids = []    
    with open(testing_data, 'r', newline ='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids.append((row['id']))

    response = client.get("/point_inputs/")
    for id in ids:
        id = id.encode('utf-8')
        assert id in response.data


#This tests that all current schools render
def test_sort_by_id_descending(client):
    #get all the names in the data
    testing_data = 'data/updated_schoolmint.csv'
    schools = []    
    with open(testing_data, 'r', newline ='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['current_school'] not in schools:
                if "'" not in row['current_school']:
                    schools.append((row['current_school']))

    response = client.get("/point_inputs/")
    for school in schools:
        school = school.encode('utf-8')
        assert school in response.data



