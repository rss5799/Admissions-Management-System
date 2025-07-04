import pytest
import random
from app.utils.csv_reader_writer import fetch_updated_student_instance
from app import create_app
from app.services.matrix_calculator import matrix, calculate_gpa, calculate_total_matrix
from app.utils.csv_riverside_writer import combine_data
import csv
import os

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
    list_of_grades.append(['A', 'A', 'B', 'D', '', 3.0])
    list_of_grades.append(['B', 'B', '', '', '', 3.0])
    list_of_grades.append(['a', 'b', 'c', 'd', 'f', 2.0])
    list_of_grades.append(['a', 'A', 'b', 'D', 'c', 2.8])
    list_of_grades.append(['1', '1', '1', '1', '1', 0])
    list_of_grades.append(['B', 'B', '1', '@', '$', 3.0])
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
    list_of_grades.append(['A', '2', 'A', 'A', '$', 95, 96, 97, 116])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', '', 99, 99, 90])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', '$', '@', '', 30])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', '^', 98, 98, 90])
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', 85.5, 90.5, 99, 86])   
    list_of_grades.append(['A', 'A', 'A', 'A', 'A', -5, 99, 99, 90]) 


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
    original_schoolmint = str('tests/SampleCsvsForTesting/schoolmintForPytest.csv')
    #make a copy of schoolmint for pytests
    if os.path.exists('tests/SampleCsvsForTesting/copyOfDataForTesting.csv'):
        os.remove('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    
    assert not os.path.exists('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    copy_for_testing = str('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    with open(original_schoolmint, 'r', newline='') as infile:
        reader = csv.reader(infile)
        with open(copy_for_testing, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)
    #open riverside for pytests
    riverside_dummy_for_pytest = ('tests/SampleCsvsForTesting/riversideForPytest.csv')
    with open(original_schoolmint, 'r', newline='') as infile:
        reader = csv.reader(infile)
        with open(copy_for_testing, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)
    #pass them into def place_riverside_into_schoolmint(schoolmintData, riversideResults)
    counter = combine_data(copy_for_testing, riverside_dummy_for_pytest)
    assert counter == 18
    with open(copy_for_testing, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        #assertions for student with GPA first test
        assert float(data[1][1]) == 1
        assert float(data[1][3]) == 88
        assert float(data[1][4]) == 95
        assert float(data[1][5]) == 91
        assert float(data[1][6])== 99
        assert float(data[1][7]) == 25
        assert float(data[1][8]) == 26
        assert float(data[1][9]) == 28
        assert data[1][11] == ''
        assert data[1][12] == ''
        assert data[1][13] == ''
        assert float(data[1][14]) == 20
        assert data[1][23] == ''
        assert data[1][24] == ''
        assert data[1][25] == ''
    #assertions for student without GPA first test
        assert float(data[2][1]) == 2
        assert float(data[2][3]) == 75
        assert float(data[2][4]) == 75
        assert float(data[2][5]) == 91
        assert float(data[2][6]) == 62
        assert float(data[2][7]) == 18
        assert float(data[2][8]) == 26
        assert float(data[2][9]) == 18
        assert data[2][11] == ''
        assert data[2][12] == ''
        assert data[2][13] == ''
        assert data[2][14] == ''
        assert data[2][23] == ''
        assert data[2][24] == ''
        assert data[2][25] == ''
    #assertions for student with GPA retest
        assert float(data[3][1]) == 3
        assert float(data[3][3]) == 76
        assert float(data[3][4]) == 85
        assert float(data[3][5]) == 76
        assert float(data[3][6]) == 87
        assert float(data[3][7]) == 19
        assert float(data[3][8]) == 19
        assert float(data[3][9]) == 23
        assert float(data[3][11]) == 26
        assert float(data[3][12]) == 19
        assert float(data[3][13]) == 22
        assert float(data[3][14]) == 93
        assert float(data[3][23]) == 91
        assert float(data[3][24]) == 83
        assert float(data[3][25]) == 76
    #assertions for student without GPA retest
        assert float(data[4][1]) == 4
        assert float(data[4][3]) == 79
        assert float(data[4][4]) == 90
        assert float(data[4][5]) == 65
        assert float(data[4][6]) == 59
        assert float(data[4][7]) == 20
        assert float(data[4][8]) == 13
        assert float(data[4][9]) == 26
        assert float(data[4][11]) == 27
        assert float(data[4][12]) == 25
        assert float(data[4][13]) == 26
        assert float(data[4][14]) == 78
        assert float(data[4][23]) == 92
        assert float(data[4][24]) == 90
        assert float(data[4][25]) == 89
    #assertions for student who had only one part of the first test 
        assert float(data[5][1]) == 5
        assert float(data[5][3]) == 83
        assert data[5][4] == ''
        assert data[5][5] == ''
        assert float(data[5][6]) == 52
        assert float(data[5][7]) == 22
        assert data[5][8] == ''
        assert data[5][9] == ''
        assert float(data[5][11]) == 12
        assert float(data[5][12]) == 23
        assert float(data[5][13]) == 17
        assert float(data[5][14]) == 82
        assert float(data[5][23]) == 63
        assert float(data[5][24]) == 72
        assert float(data[5][25]) == 85
    #assertions for student who had first test and retest and GPA
        assert float(data[6][1]) == 6
        assert float(data[6][3]) == 70
        assert float(data[6][4]) == 75
        assert float(data[6][5]) == 77
        assert float(data[6][6]) == 75
        assert float(data[6][7]) == 16
        assert float(data[6][8]) == 19
        assert float(data[6][9]) == 18
        assert float(data[6][11]) == 26
        assert float(data[6][12]) == 25
        assert float(data[6][13]) == 26
        assert float(data[6][14]) == 99
        assert float(data[6][23]) == 91
        assert float(data[6][24]) == 91
        assert float(data[6][25]) == 88
    #assertions for student who had first test and retest without GPA
        assert float(data[7][1]) == 7
        assert float(data[7][3]) == 66
        assert float(data[7][4]) == 72
        assert float(data[7][5]) == 62
        assert float(data[7][6]) == 43
        assert float(data[7][7]) == 14
        assert float(data[7][8]) == 12
        assert float(data[7][9]) == 17
        assert float(data[7][11]) == 22
        assert float(data[7][12]) == 23
        assert float(data[7][13]) == 22
        assert float(data[7][14]) == 67
        assert float(data[7][23]) == 82
        assert float(data[7][24]) == 83
        assert float(data[7][25]) == 84
    # #assertsions for student who wasn't already in schoolmint
        assert data[8][1] == ''
        assert float(data[8][3]) == 89
        assert float(data[8][4]) == 93
        assert float(data[8][5]) == 88
        assert float(data[8][6]) == 77
        assert float(data[8][7]) == 25
        assert float(data[8][8]) == 25
        assert float(data[8][9]) == 27
        assert data[8][11] == ''
        assert data[8][12] == ''
        assert data[8][13] == ''
        assert data[8][14] == ''
        assert data[8][23] == ''
        assert data[8][24] == ''
        assert data[8][25] == ''
    # #assertions for student who had no test scores returned
        assert float(data[9][1]) == 9
        assert float(data[9][3]) == 89
        assert float(data[9][4]) == 93
        assert float(data[9][5]) == 88
        assert float(data[9][6]) == 77
        assert float(data[9][7]) == 25
        assert float(data[9][8]) == 25
        assert float(data[9][9]) == 27
        assert float(data[9][11]) == 0
        assert float(data[9][12]) == 0
        assert float(data[9][13]) == 0
        assert float(data[9][14]) == 0
        assert float(data[9][23]) == 0
        assert float(data[9][24]) == 0
        assert float(data[9][25]) == 0
    # #assertions for student who had invalid data in riverside file
        assert float(data[10][1]) == 10
        assert float(data[10][3]) == 65
        assert float(data[10][4]) == 0
        assert float(data[10][5]) == 80
        assert float(data[10][6]) == 34
        assert float(data[10][7]) == 13
        assert float(data[10][8]) == 21
        assert float(data[10][9]) == 0
        assert data[10][11] == ''
        assert data[10][12] == ''
        assert data[10][13] == ''
        assert data[10][14] == ''
        assert data[10][23] == ''
        assert data[10][24] == ''
        assert data[10][25] == ''
    # #assertions for student who had partial test scores returned for retest
        assert float(data[11][1]) == 11
        assert float(data[11][3]) == 70
        assert float(data[11][4]) == 65
        assert float(data[11][5]) == 75
        assert float(data[11][6]) == 67
        assert float(data[11][7]) == 16
        assert float(data[11][8]) == 18
        assert float(data[11][9]) == 13
        assert float(data[11][11]) == 0
        assert float(data[11][12]) == 21
        assert float(data[11][13]) == 15
        assert float(data[11][14]) == 56
        assert float(data[11][23]) == 0
        assert float(data[11][24]) == 69
        assert float(data[11][25]) == 81
# #assertions for student who had partial test scores returned for retest
        assert float(data[12][1]) == 12
        assert float(data[12][3]) == 88
        assert float(data[12][4]) == 87
        assert float(data[12][5]) == 0
        assert float(data[12][6]) == 49
        assert float(data[12][7]) == 25
        assert float(data[12][8]) == 0
        assert float(data[12][9]) == 24
        assert data[12][11] == ''
        assert data[12][12] == ''
        assert data[12][13] == ''
        assert data[12][14] == ''
        assert data[12][23] == ''
        assert data[12][24] == ''
        assert data[12][25] == ''
    # #assertions for student who had partial test scores returned for retest
        assert float(data[14][1]) == 14
        assert float(data[14][3]) == 76
        assert float(data[14][4]) == 88
        assert float(data[14][5]) == 82
        assert float(data[14][6]) == 66
        assert float(data[14][7]) == 19
        assert float(data[14][8]) == 22
        assert float(data[14][9]) == 25
        assert float(data[14][11]) == 0
        assert float(data[14][12]) == 23
        assert float(data[14][13]) == 0
        assert float(data[14][14]) == 23
        assert float(data[14][23]) == 0
        assert float(data[14][24]) == 0
        assert float(data[14][25]) == 85
        # #assertions for student who had partial test scores returned for first test
        assert float(data[15][1]) == 15
        assert float(data[15][3]) == 65
        assert float(data[15][4]) == 0
        assert float(data[15][5]) == 0
        assert float(data[15][6]) == 13
        assert float(data[15][7]) == 13
        assert float(data[15][8]) == 0
        assert float(data[15][9]) == 0
        assert data[15][11] == ''
        assert data[15][12] == ''
        assert data[15][13] == ''
        assert data[15][14] == ''
        assert data[15][23] == ''
        assert data[15][24] == ''
        assert data[15][25] == ''
    # #assertions for student who had partial test scores returned for first test
        assert float(data[16][1]) == 16
        assert float(data[16][3]) == 0
        assert float(data[16][4]) == 88
        assert float(data[16][5]) == 0
        assert float(data[16][6]) == 25
        assert float(data[16][7]) == 0
        assert float(data[16][8]) == 0
        assert float(data[16][9]) == 25
        assert data[16][11] == ''
        assert data[16][12] == ''
        assert data[16][13] == ''
        assert data[16][14] == ''
        assert data[16][23] == ''
        assert data[16][24] == ''
        assert data[16][25] == ''
        # #assertions for student who had partial test scores returned for retest
        assert float(data[17][1]) == 17
        assert float(data[17][3]) == 85
        assert float(data[17][4]) == 80
        assert float(data[17][5]) == 82
        assert float(data[17][6]) == 87
        assert float(data[17][7]) == 23
        assert float(data[17][8]) == 22
        assert float(data[17][9]) == 21
        assert float(data[17][11]) == 0
        assert float(data[17][12]) == 0
        assert float(data[17][13]) == 0
        assert float(data[17][14]) == 21
        assert float(data[17][23]) == 0
        assert float(data[17][24]) == 0
        assert float(data[17][25]) == 0
# #assertions for student who had partial test scores returned for first test
        assert float(data[18][1]) == 18
        assert float(data[18][3]) == 90
        assert float(data[18][4]) == 90
        assert float(data[18][5]) == 0
        assert float(data[18][6]) == 52
        assert float(data[18][7]) == 26
        assert float(data[18][8]) == 0
        assert float(data[18][9]) == 26
        assert data[18][11] == ''
        assert data[18][12] == ''
        assert data[18][13] == ''
        assert data[18][14] == ''
        assert data[18][23] == ''
        assert data[18][24] == ''
        assert data[18][25] == ''
# #assertions for student who had partial test scores returned for first test
        assert float(data[19][1]) == 19
        assert float(data[19][3]) == 90
        assert float(data[19][4]) == 0
        assert float(data[19][5]) == 87
        assert float(data[19][6]) == 50
        assert float(data[19][7]) == 26
        assert float(data[19][8]) == 24
        assert float(data[19][9]) == 0
        assert data[19][11] == ''
        assert data[19][12] == ''
        assert data[19][13] == ''
        assert data[19][14] == ''
        assert data[19][23] == ''
        assert data[19][24] == ''
        assert data[19][25] == ''
# #assertions for student who had partial test scores returned for retest
        assert float(data[20][1]) == 20
        assert float(data[20][3]) == 78
        assert float(data[20][4]) == 78
        assert float(data[20][5]) == 78
        assert float(data[20][6]) == 82
        assert float(data[20][7]) == 20
        assert float(data[20][8]) == 20
        assert float(data[20][9]) == 20
        assert float(data[20][11]) == 0
        assert float(data[20][12]) == 24
        assert float(data[20][13]) == 19
        assert float(data[20][14]) == 65
        assert float(data[20][23]) == 0
        assert float(data[20][24]) == 77
        assert float(data[20][25]) == 87





