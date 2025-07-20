import pandas as pd
import pytest
from app import create_app
import csv
from pathlib import Path
from flask.testing import FlaskClient
from app.services.filtering import DataFilter
from app.services.sorting import apply_sorting 


# fixtures
@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def student_data_df():
    csv_path = Path(__file__).resolve().parent / "SampleCsvsForTesting" / "schoolmintForPytest.csv"
    return pd.read_csv(csv_path)

# continuing tests writing

# UT-21 Verifies correct unique values per field for drop down filtering
def test_ut_21_filter_field():
    filter = DataFilter(student_data_df)
    for field in ['grade', 'status', 'test_date_sign_up']:
        _, values = filter.apply(field, None)
        assert sorted(values) == sorted(student_data_df[field].dropna().astype(str).unique().tolist())

# UT-22 Ensures filtering returns only matched records and unfilter results
def test_ut_22_filter_value():
    filter = DataFilter(student_data_df)
    filtered_df, _ = filter.apply('grade', '10th')
    assert all(filtered_df['grade'] == '10th')
    unfiltered_df, _ = filter.apply(None, None)
    assert len(unfiltered_df) == len(student_data_df)   
    
# ST-26 Test Flask route with query string filtering with FlaskClient
def test_st_26_filter_input(client: FlaskClient):
    response = client.get('/point_inputs?filter_field=grade&filter_value=10th')
    assert response.status_code == 200
    assert b'10th' in response.data # tests it's included
    assert b'11th' not in response.data # tests it's not included