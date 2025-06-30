import pytest
from flask import render_template
import random
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance, write_gpa_to_csv
from app import create_app
from app.services.matrix_calculator import lookup_matrix_points, matrix, calculate_gpa, calculate_total_matrix
from app.csv_utils.csv_riverside_writer import combine_data, place_riverside_into_schoolmint
import json
import csv

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


#Unit Test 11: Ensure that calculate gpa function turns out the correct value
def test_calculate_gpa():
    grades = {
        "english": "",
        "math": "",
        "science": "",
        "social_studies": "",
        "language": ""
    }

    list_of_grades = []
    list_of_grades.append(['A', 'B', 'C', 'D', 'F', 2.0])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', 4.0])
    #list_of_grades.append(['A', 'A', 'B', 'D', '', 3.0])
    #list_of_grades.append(['B', 'B', '', '', '', 3.0])
    list_of_grades.append(['a', 'b', 'c', 'd', 'f', 2.0])
    list_of_grades.append(['a', 'A', 'b', 'D', 'c', 2.8])
    list_of_grades.append(['1', '1', '1', '1', '1', 0])
    #list_of_grades.append(['B', 'B', '1', '@', '$', 3.0])
    list_of_grades.append(['1', '#', '@', '!', '*', 0])

    #for course in grades:
    for item in list_of_grades:
        grades['english'] = item[0]
        grades['math'] = item[1]
        grades['science'] = item[2]
        grades['social_studies'] = item[3]
        grades['language'] = item[4]
        gpa = item[5]
        assert gpa == calculate_gpa(grades)




#Unit Test 12:  Ensure total matrix value is accurately returned
def test_calculate_total_matrix():
    grades = {
        "english": "",
        "math": "",
        "science": "",
        "social_studies": "",
        "language": ""
    }

    list_of_grades = []
    list_of_grades.append(['A', 'B', 'C', 'D', 'F', 98, 98, 98, 105])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', 50, 60, 70, 63])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', 0, 0, 0, 30])
    #list_of_grades.append(['A', '2', 'A', 'A', '$', 95, 96, 97, 0])
    #list_of_grades.append(['A', 'A', 'A', 'A', 'A', '', 99, 99, 0])
    #list_of_grades.append(['A', 'A', 'A', 'A', 'A', '$', '@', '', 0])
    #list_of_grades.append(['A', 'A', 'A', 'A', 'A', '^', 98, 98, 0])
    #list_of_grades.append(['A', 'A', 'A', 'A', 'A', 85.5, 90.5, 99, 0])   
    #list_of_grades.append(['A', 'A', 'A', 'A', 'A', -5, 99, 99, 0]) 


    #for course in grades:
    for item in list_of_grades:
        grades['english'] = item[0]
        grades['math'] = item[1]
        grades['science'] = item[2]
        grades['social_studies'] = item[3]
        grades['language'] = item[4]
        reading = item[5]
        language = item[6]
        math = item[7]
        matrix_expected = item[8]

        assert calculate_total_matrix(grades, reading, language, math)['total_matrix_score'] == matrix_expected




# # # # #System Test 16: Ensure that total matrix points persist to file export page.
def test_matrix_points_persist_to_export(client):
    #get 5 random students ids
    random_students = [random.randint(1, 2000) for _ in range(5)]
    #iterate through the students
    for student_id in random_students:
        student = fetch_updated_student_instance(student_id)
        if student != 0:
            matrix_score = student.total_points
            response = client.get("/exports/")
            student = fetch_updated_student_instance(student_id)
            if student != 0:
                assert response.status_code == 200
                assert b"Exports" in response.data
                assert matrix_score == student.total_points


#System Test 17: Ensure riverside scores are being transfered and calculated correctly

def test_riverside_data_transfer():
    #open original schoolmint for pytests
    original_schoolmint = str('tests/schoolmintForPytest.csv')
    #make a copy of schoolmint for pytests
    copy_for_testing = str('tests/copyOfDataForTesting.csv')
    with open(original_schoolmint, 'r', newline='') as infile:
        reader = csv.reader(infile)
        with open(copy_for_testing, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)
    #open riverside for pytests
    riverside_dummy_for_pytest = ('tests/riversideForPytest.csv')
    #pass them into def place_riverside_into_schoolmint(schoolmintData, riversideResults)
    place_riverside_into_schoolmint(copy_for_testing, riverside_dummy_for_pytest)
    counter = combine_data(copy_for_testing, riverside_dummy_for_pytest)
    with open(copy_for_testing, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        #assertions for student with GPA first test
        assert data[1][1] == '1.0'
        assert data[1][3] == '88.0'
        assert data[1][4] == '95.0'
        assert data[1][5] == '91.0'
        assert data[1][6] == '99.0'
        assert data[1][7] == '25'
        assert data[1][8] == '26'
        assert data[1][9] == '28'
        assert data[1][11] == ''
        assert data[1][12] == ''
        assert data[1][13] == ''
        assert data[1][14] == '20.0'
        assert data[1][23] == ''
        assert data[1][24] == ''
        assert data[1][25] == ''
    #assertions for student without GPA first test
        assert data[2][1] == '2.0'
        assert data[2][3] == '75.0'
        assert data[2][4] == '75.0'
        assert data[2][5] == '91.0'
        assert data[2][6] == '62'
        assert data[2][7] == '18'
        assert data[2][8] == '26'
        assert data[2][9] == '18'
        assert data[2][11] == ''
        assert data[2][12] == ''
        assert data[2][13] == ''
        assert data[2][14] == ''
        assert data[2][23] == ''
        assert data[2][24] == ''
        assert data[2][25] == ''
    #assertions for student with GPA retest
        assert data[3][1] == '3.0'
        assert data[3][3] == '76.0'
        assert data[3][4] == '85.0'
        assert data[3][5] == '76.0'
        assert data[3][6] == '87.0'
        assert data[3][7] == '19.0'
        assert data[3][8] == '19.0'
        assert data[3][9] == '23.0'
        assert data[3][11] == '26'
        assert data[3][12] == '19'
        assert data[3][13] == '22'
        assert data[3][14] == '93.0'
        assert data[3][23] == '91.0'
        assert data[3][24] == '83.0'
        assert data[3][25] == '76.0'
    #assertions for student without GPA retest
        assert data[4][1] == '4.0'
        assert data[4][3] == '79.0'
        assert data[4][4] == '90.0'
        assert data[4][5] == '65.0'
        assert data[4][6] == '59.0'
        assert data[4][7] == '20.0'
        assert data[4][8] == '13.0'
        assert data[4][9] == '26.0'
        assert data[4][11] == '27'
        assert data[4][12] == '25'
        assert data[4][13] == '26'
        assert data[4][14] == '78'
        assert data[4][23] == '92.0'
        assert data[4][24] == '90.0'
        assert data[4][25] == '89.0'
    #assertions for student who had only one part of the first test 
        assert data[5][1] == '5.0'
        assert data[5][3] == '83.0'
        assert data[5][4] == ''
        assert data[5][5] == ''
        assert data[5][6] == '52.0'
        assert data[5][7] == '22.0'
        assert data[5][8] == ''
        assert data[5][9] == ''
        assert data[5][11] == '12'
        assert data[5][12] == '23'
        assert data[5][13] == '17'
        assert data[5][14] == '82.0'
        assert data[5][23] == '63.0'
        assert data[5][24] == '72.0'
        assert data[5][25] == '85.0'
    #assertions for student who had first test and retest and GPA
        assert data[6][1] == '6.0'
        assert data[6][3] == '70.0'
        assert data[6][4] == '75.0'
        assert data[6][5] == '77.0'
        assert data[6][6] == '75.0'
        assert data[6][7] == '16.0'
        assert data[6][8] == '19.0'
        assert data[6][9] == '18.0'
        assert data[6][11] == '26.0'
        assert data[6][12] == '25.0'
        assert data[6][13] == '26.0'
        assert data[6][14] == '99.0'
        assert data[6][23] == '91.0'
        assert data[6][24] == '91.0'
        assert data[6][25] == '88.0'
    #assertions for student who had first test and retest without GPA
        assert data[7][1] == '7.0'
        assert data[7][3] == '66.0'
        assert data[7][4] == '72.0'
        assert data[7][5] == '62.0'
        assert data[7][6] == '43.0'
        assert data[7][7] == '14.0'
        assert data[7][8] == '12.0'
        assert data[7][9] == '17.0'
        assert data[7][11] == '22.0'
        assert data[7][12] == '23.0'
        assert data[7][13] == '22.0'
        assert data[7][14] == '67.0'
        assert data[7][23] == '82.0'
        assert data[7][24] == '83.0'
        assert data[7][25] == '84.0'
    # #assertsions for student who wasn't already in schoolmint
        assert data[8][1] == ''
        assert data[8][3] == '89.0'
        assert data[8][4] == '93.0'
        assert data[8][5] == '88.0'
        assert data[8][6] == '77'
        assert data[8][7] == '25'
        assert data[8][8] == '25'
        assert data[8][9] == '27'
        assert data[8][11] == ''
        assert data[8][12] == ''
        assert data[8][13] == ''
        assert data[8][14] == ''
        assert data[8][23] == ''
        assert data[8][24] == ''
        assert data[8][25] == ''
    # #assertions for student who had no test scores returned
        assert data[9][1] == '9.0'
        assert data[9][3] == '89.0'
        assert data[9][4] == '93.0'
        assert data[9][5] == '88.0'
        assert data[9][6] == '77.0'
        assert data[9][7] == '25.0'
        assert data[9][8] == '25.0'
        assert data[9][9] == '27.0'
        assert data[9][11] == ''
        assert data[9][12] == ''
        assert data[9][13] == ''
        assert data[9][14] == '0'
        assert data[9][23] == ''
        assert data[9][24] == ''
        assert data[9][25] == ''



