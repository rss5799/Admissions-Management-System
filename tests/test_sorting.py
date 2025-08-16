import pytest
import csv
from app import create_app
import requests
from tests.test_utils.table_parser import AdvancedTableParser
import pandas as pd
from app.services.sorting import apply_sorting

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


sample_table = """ 
<table id = "data"> 
<thead> 
<tr><th>id</th><th>name</th></tr> 
</thead> 
<tbody> 
<tr><td>1</td><td>Alice</td></tr> 
<tr><td>2</td><td>Bob</td></tr> 
</tbody> 
</table> 
"""

sample_df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "id": [1, 2, 3],
    "SCHOOL": ["X", "Y", "Z"]
})

def test_sort_id_descending(): 
    parser = AdvancedTableParser(sample_table) 
    assert parser.is_column_sorted("id") is True

def test_sort_name_ascending():
    parser = AdvancedTableParser(sample_table)
    assert parser.is_column_sorted("name") is True

def test_sort_school_descending(client):
    response = client.get("/point_inputs/")
    assert response.status_code == 200