import pytest
from app.routes import retrieve_current_student, turn_na_to_emptystring
import pandas as pd
import numpy as np
import random
import string
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

#System Test 1: Search results are returned when valid student ID is entered
def test_search_for_student():
    assert retrieve_current_student(1) != 0
    assert retrieve_current_student(1077) != 0
    assert retrieve_current_student(1078) == 0
    assert retrieve_current_student('$') == 0
    assert retrieve_current_student(' 87') == 0
    assert retrieve_current_student('99 ') == 0
    assert retrieve_current_student(2/2) == 0
    assert retrieve_current_student('a') == 0

test_search_for_student()


#System Test 2: NaN values are converted to empty string before rendering html
def display_empty_values():
    student_df = pd.read_csv('DummyDataComplete.csv')
    #find the location of all cells missing data
    nan_locations = []
    for row in range(student_df.shape[0]):
        for col in range(student_df.shape[1]):
            if pd.isna(student_df.iloc[row, col]):
                nan_locations.append((row, col))
    #choose 10 random nan cells to test
    testing_cells = random.sample(nan_locations, min(10, len(nan_locations)))
    #iterate through the 10 cells and assert that nan converts to empty string
    for i in range(0, 10):
        id = student_df.iloc[testing_cells[i][0], 0]
        #this statement is kind of just affirming what i asked it to do when i created the testing_cells
        assert np.isnan(student_df.iloc[testing_cells[i]])
        testing_student = retrieve_current_student(id)
        turn_na_to_emptystring(testing_student)
        attribute_to_test  = str(student_df.columns[testing_cells[i][1]])
        value = str(getattr(testing_student, attribute_to_test))
        assert value == ""
display_empty_values()


#System Test 3: Display Real-Time Updates in Detail View
#Happy path: write a change to the csv which reflects when the student search is completed
def display_updates_to_csv():
    student_df = pd.read_csv('DummyDataComplete.csv')
    student_df = student_df.astype(str)
    student_df_modified = student_df.copy()

    #choose 100 random cells and store them in a list of tuples called results (row, column, value)
    rows = np.random.choice(student_df.index, size=100)
    cols = np.random.choice(student_df.columns, size=100)

    results = []
    for row, col in zip(rows, cols):
        results.append((row, col, student_df.loc[row, col]))

    #make a list of student IDs that are modified
    ids_modified = []
    for item in results:
        row = item[0]
        id = student_df.iloc[row, 0]
        ids_modified.append(id)
    
    #make a new list of tuples where the same cells are chosen but a random value replaces the third value
    new_results = []
    for tuple_item in results:
        temp_list = list(tuple_item)
        characters = string.ascii_letters + string.digits
        rand_string = ''.join(random.choice(characters) for _ in range(4))
        temp_list[2] = rand_string
        new_results.append(tuple(temp_list))
    #put the newly generated random string into the new modified dataframe
    for row, col, new_val in new_results:
        student_df_modified.loc[row, col] = new_val
    #save the silly dataframe
    student_df_modified.to_csv('new_data_file.csv', index=False)
    #iterate through the results from the OG dataframe and assert they're different than the silly dataframe
    for result in results:
        for new_result in new_results:
            assert student_df.loc[result[0], result[1]] != student_df_modified.loc[new_result[0], new_result[1]]

def test_student_search_no_param(client):
    response = client.get("/student_details/")
    assert response.status_code == 200
    assert b"student_details" in response.data

def test_student_search_invalid_id(client):
    response = client.get("/student_details/?id_query=NOT_A_REAL_ID")
    assert response.status_code == 200
    assert b"student_details" in response.data


display_updates_to_csv()
        
