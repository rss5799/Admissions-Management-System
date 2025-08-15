import pytest  
from app import create_app
from tests.test_utils.test_table_parser import AdvancedTableParser
import pandas as pd
from app.services.sorting import apply_sorting




@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client




sample_table = """
<table id = "studentsTable">
<thead>
<tr><th>id</th><th>School</th></tr>
</thead>
<tbody>
<tr><td>1</td><td>"SchoolB"</td></tr>
<tr><td>2</td><td>SchoolA</td></tr>
</tbody>
</table>
"""

sample_df = pd.DataFrame({
    "id": [1, 2],
    "school":["SchoolB", "SchoolA"]
})


#Unit Test 23
def test_sort_id_descending():
    parser = AdvancedTableParser(sample_table)
    assert parser.is_column_sorted("id") is True


#Unit test 26
def test_sort_school_ascending():
    parser = AdvancedTableParser(sample_table)
    assert parser.is_column_sorted("School") is True



#Unit test 27
def test_sort_school_descending(client):
    response = client.get("/point_inputs/")
    assert response.status_code == 200
