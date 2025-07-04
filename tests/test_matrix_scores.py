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




#System Test 16: Ensure that total matrix points persist to file export page.
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
    original_schoolmint = ('tests/SampleCsvsForTesting/schoolmintForPytest.csv')
    #make a copy of schoolmint for pytests
    if os.path.exists('tests/SampleCsvsForTesting/copyOfDataForTesting.csv'):
        os.remove('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    
    assert not os.path.exists('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    copy_for_testing = ('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
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
        header = next(reader)
        data = list(reader)
        #assertions for student with GPA first test
        assert float(data[0][header.index('id')]) == 1
        assert float(data[0][header.index('language_test_scores')]) == 88
        assert float(data[0][header.index('reading_test_score')]) == 95
        assert float(data[0][header.index('math_test_scores')]) == 91
        assert float(data[0][header.index('total_points')])== 99
        assert float(data[0][header.index('matrix_languauge')]) == 25
        assert float(data[0][header.index('matrix_math')]) == 26
        assert float(data[0][header.index('matrix_reading')]) == 28
        assert data[0][header.index('matrix_languauge_retest')] == ''
        assert data[0][header.index('matrix_math_retest')] == ''
        assert data[0][header.index('matrix_reading_restest')] == ''
        assert float(data[0][header.index('total_points_retest')]) == 20
        assert data[0][header.index('language_test_scores2')] == ''
        assert data[0][header.index('reading_test_score2')] == ''
        assert data[0][header.index('math_test_scores2')] == ''
    #assertions for student without GPA first test
        assert float(data[1][header.index('id')]) == 2
        assert float(data[1][header.index('language_test_scores')]) == 75
        assert float(data[1][header.index('reading_test_score')]) == 75
        assert float(data[1][header.index('math_test_scores')]) == 91
        assert float(data[1][header.index('total_points')])== 62
        assert float(data[1][header.index('matrix_languauge')]) == 18
        assert float(data[1][header.index('matrix_math')]) == 26
        assert float(data[1][header.index('matrix_reading')]) == 18
        assert data[1][header.index('matrix_languauge_retest')] == ''
        assert data[1][header.index('matrix_math_retest')] == ''
        assert data[1][header.index('matrix_reading_restest')] == ''
        assert data[1][header.index('total_points_retest')] == ''
        assert data[1][header.index('language_test_scores2')] == ''
        assert data[1][header.index('reading_test_score2')] == ''
        assert data[1][header.index('math_test_scores2')] == ''
    #assertions for student with GPA retest
        assert float(data[2][header.index('id')]) == 3
        assert float(data[2][header.index('language_test_scores')]) == 76
        assert float(data[2][header.index('reading_test_score')]) == 85
        assert float(data[2][header.index('math_test_scores')]) == 76
        assert float(data[2][header.index('total_points')])== 87
        assert float(data[2][header.index('matrix_languauge')]) == 19
        assert float(data[2][header.index('matrix_math')]) == 19
        assert float(data[2][header.index('matrix_reading')]) == 23
        assert float(data[2][header.index('matrix_languauge_retest')]) == 26
        assert float(data[2][header.index('matrix_math_retest')]) == 19
        assert float(data[2][header.index('matrix_reading_restest')]) == 22
        assert float(data[2][header.index('total_points_retest')]) == 93
        assert float(data[2][header.index('language_test_scores2')]) == 91
        assert float(data[2][header.index('reading_test_score2')]) == 83
        assert float(data[2][header.index('math_test_scores2')]) == 76
    #assertions for student without GPA retest
        assert float(data[3][header.index('id')]) == 4
        assert float(data[3][header.index('language_test_scores')]) == 79
        assert float(data[3][header.index('reading_test_score')]) == 90
        assert float(data[3][header.index('math_test_scores')]) == 65
        assert float(data[3][header.index('total_points')])== 59
        assert float(data[3][header.index('matrix_languauge')]) == 20
        assert float(data[3][header.index('matrix_math')]) == 13
        assert float(data[3][header.index('matrix_reading')]) == 26
        assert float(data[3][header.index('matrix_languauge_retest')]) == 27
        assert float(data[3][header.index('matrix_math_retest')]) == 25
        assert float(data[3][header.index('matrix_reading_restest')]) == 26
        assert float(data[3][header.index('total_points_retest')]) == 78
        assert float(data[3][header.index('language_test_scores2')]) == 92
        assert float(data[3][header.index('reading_test_score2')]) == 90
        assert float(data[3][header.index('math_test_scores2')]) == 89
    #assertions for student who had only one part of the first test 
        assert float(data[4][header.index('id')]) == 5
        assert float(data[4][header.index('language_test_scores')]) ==83
        assert data[4][header.index('reading_test_score')] == ''
        assert data[4][header.index('math_test_scores')] == ''
        assert float(data[4][header.index('total_points')])== 52
        assert float(data[4][header.index('matrix_languauge')]) == 22
        assert data[4][header.index('matrix_math')] == ''
        assert data[4][header.index('matrix_reading')] == ''
        assert float(data[4][header.index('matrix_languauge_retest')]) == 12
        assert float(data[4][header.index('matrix_math_retest')]) == 23
        assert float(data[4][header.index('matrix_reading_restest')]) == 17
        assert float(data[4][header.index('total_points_retest')]) == 82
        assert float(data[4][header.index('language_test_scores2')]) == 63
        assert float(data[4][header.index('reading_test_score2')]) == 72
        assert float(data[4][header.index('math_test_scores2')]) == 85
    #assertions for student who had first test and retest and GPA
        assert float(data[5][header.index('id')]) == 6
        assert float(data[5][header.index('language_test_scores')]) == 70
        assert float(data[5][header.index('reading_test_score')]) == 75
        assert float(data[5][header.index('math_test_scores')]) == 77
        assert float(data[5][header.index('total_points')])== 75
        assert float(data[5][header.index('matrix_languauge')]) == 16
        assert float(data[5][header.index('matrix_math')]) == 19
        assert float(data[5][header.index('matrix_reading')]) == 18
        assert float(data[5][header.index('matrix_languauge_retest')]) == 26
        assert float(data[5][header.index('matrix_math_retest')]) == 25
        assert float(data[5][header.index('matrix_reading_restest')]) == 26
        assert float(data[5][header.index('total_points_retest')]) == 99
        assert float(data[5][header.index('language_test_scores2')]) == 91
        assert float(data[5][header.index('reading_test_score2')]) == 91
        assert float(data[5][header.index('math_test_scores2')]) == 88
    #assertions for student who had first test and retest without GPA
        assert float(data[6][header.index('id')]) == 7
        assert float(data[6][header.index('language_test_scores')]) == 66
        assert float(data[6][header.index('reading_test_score')]) == 72
        assert float(data[6][header.index('math_test_scores')]) == 62
        assert float(data[6][header.index('total_points')])== 43
        assert float(data[6][header.index('matrix_languauge')]) == 14
        assert float(data[6][header.index('matrix_math')]) == 12
        assert float(data[6][header.index('matrix_reading')]) == 17
        assert float(data[6][header.index('matrix_languauge_retest')]) == 22
        assert float(data[6][header.index('matrix_math_retest')]) == 23
        assert float(data[6][header.index('matrix_reading_restest')]) == 22
        assert float(data[6][header.index('total_points_retest')]) == 67
        assert float(data[6][header.index('language_test_scores2')]) == 82
        assert float(data[6][header.index('reading_test_score2')]) == 83
        assert float(data[6][header.index('math_test_scores2')]) == 84
    # #assertsions for student who wasn't already in schoolmint
        assert data[7][header.index('id')] == ''
        assert float(data[7][header.index('language_test_scores')]) == 89
        assert float(data[7][header.index('reading_test_score')]) == 93
        assert float(data[7][header.index('math_test_scores')]) == 88
        assert float(data[7][header.index('total_points')])== 77
        assert float(data[7][header.index('matrix_languauge')]) == 25
        assert float(data[7][header.index('matrix_math')]) == 25
        assert float(data[7][header.index('matrix_reading')]) == 27
        assert data[7][header.index('matrix_languauge_retest')] == ''
        assert data[7][header.index('matrix_math_retest')] == ''
        assert data[7][header.index('matrix_reading_restest')] == ''
        assert data[7][header.index('total_points_retest')] == ''
        assert data[7][header.index('language_test_scores2')] == ''
        assert data[7][header.index('reading_test_score2')] == ''
        assert data[7][header.index('math_test_scores2')] == ''
    # #assertions for student who had no test scores returned
        assert float(data[8][header.index('id')])== 9
        assert float(data[8][header.index('language_test_scores')]) == 89
        assert float(data[8][header.index('reading_test_score')]) == 93
        assert float(data[8][header.index('math_test_scores')]) == 88
        assert float(data[8][header.index('total_points')])== 77
        assert float(data[8][header.index('matrix_languauge')]) == 25
        assert float(data[8][header.index('matrix_math')]) == 25
        assert float(data[8][header.index('matrix_reading')]) == 27
        assert data[8][header.index('matrix_languauge_retest')] == ''
        assert data[8][header.index('matrix_math_retest')] == ''
        assert data[8][header.index('matrix_reading_restest')] == ''
        assert float(data[8][header.index('total_points_retest')]) == 0
        assert data[8][header.index('language_test_scores2')] == ''
        assert data[8][header.index('reading_test_score2')] == ''
        assert data[8][header.index('math_test_scores2')] == ''
    # #assertions for student who had invalid data in riverside file
        assert float(data[9][header.index('id')])== 10
        assert float(data[9][header.index('language_test_scores')]) == 65
        assert data[9][header.index('reading_test_score')] == ''
        assert float(data[9][header.index('math_test_scores')]) == 80
        assert float(data[9][header.index('total_points')])== 34
        assert float(data[9][header.index('matrix_languauge')]) == 13
        assert float(data[9][header.index('matrix_math')]) == 21
        assert data[9][header.index('matrix_reading')] == ''
        assert data[9][header.index('matrix_languauge_retest')] == ''
        assert data[9][header.index('matrix_math_retest')] == ''
        assert data[9][header.index('matrix_reading_restest')] == ''
        assert data[9][header.index('total_points_retest')] == ''
        assert data[9][header.index('language_test_scores2')] == ''
        assert data[9][header.index('reading_test_score2')] == ''
        assert data[9][header.index('math_test_scores2')] == ''
    # #assertions for student who had partial test scores returned for retest
        assert float(data[10][header.index('id')])== 11
        assert float(data[10][header.index('language_test_scores')]) == 70
        assert float(data[10][header.index('reading_test_score')]) == 65
        assert float(data[10][header.index('math_test_scores')]) == 75
        assert float(data[10][header.index('total_points')])== 67
        assert float(data[10][header.index('matrix_languauge')]) == 16
        assert float(data[10][header.index('matrix_math')]) == 18
        assert float(data[10][header.index('matrix_reading')]) == 13
        assert data[10][header.index('matrix_languauge_retest')] == ''
        assert float(data[10][header.index('matrix_math_retest')]) == 21
        assert float(data[10][header.index('matrix_reading_restest')]) == 15
        assert float(data[10][header.index('total_points_retest')]) == 56
        assert data[10][header.index('language_test_scores2')] == ''
        assert float(data[10][header.index('reading_test_score2')]) == 69
        assert float(data[10][header.index('math_test_scores2')]) == 81
# #assertions for student who had partial test scores returned for retest
        assert float(data[11][header.index('id')])== 12
        assert float(data[11][header.index('language_test_scores')]) == 88
        assert float(data[11][header.index('reading_test_score')]) == 87
        assert data[11][header.index('math_test_scores')] == ''
        assert float(data[11][header.index('total_points')])== 49
        assert float(data[11][header.index('matrix_languauge')]) == 25
        assert data[11][header.index('matrix_math')] == ''
        assert float(data[11][header.index('matrix_reading')]) == 24
        assert data[11][header.index('matrix_languauge_retest')] == ''
        assert data[11][header.index('matrix_math_retest')] == ''
        assert data[11][header.index('matrix_reading_restest')] == ''
        assert data[11][header.index('total_points_retest')] == ''
        assert data[11][header.index('language_test_scores2')] == ''
        assert data[11][header.index('reading_test_score2')] == ''
        assert data[11][header.index('math_test_scores2')] == '' 
    # #assertions for student who had partial test scores returned for retest
        assert float(data[13][header.index('id')])== 14
        assert float(data[13][header.index('language_test_scores')]) == 76
        assert float(data[13][header.index('reading_test_score')]) == 88
        assert float(data[13][header.index('math_test_scores')]) == 82
        assert float(data[13][header.index('total_points')])== 66
        assert float(data[13][header.index('matrix_languauge')]) == 19
        assert float(data[13][header.index('matrix_math')]) == 22
        assert float(data[13][header.index('matrix_reading')]) == 25
        assert data[13][header.index('matrix_languauge_retest')] == ''
        assert float(data[13][header.index('matrix_math_retest')]) == 23
        assert data[13][header.index('matrix_reading_restest')] == ''
        assert float(data[13][header.index('total_points_retest')]) == 23
        assert data[13][header.index('language_test_scores2')] == ''
        assert data[13][header.index('reading_test_score2')] == ''
        assert float(data[13][header.index('math_test_scores2')]) == 85
        # #assertions for student who had partial test scores returned for first test
        assert float(data[14][header.index('id')])== 15
        assert float(data[14][header.index('language_test_scores')]) == 65
        assert data[14][header.index('reading_test_score')] == ''
        assert data[14][header.index('math_test_scores')] == ''
        assert float(data[14][header.index('total_points')])== 13
        assert float(data[14][header.index('matrix_languauge')]) == 13
        assert data[14][header.index('matrix_math')] == ''
        assert data[14][header.index('matrix_reading')] == ''
        assert data[14][header.index('matrix_languauge_retest')] == ''
        assert data[14][header.index('matrix_math_retest')] == ''
        assert data[14][header.index('matrix_reading_restest')] == ''
        assert data[14][header.index('total_points_retest')] == ''
        assert data[14][header.index('language_test_scores2')] == ''
        assert data[14][header.index('reading_test_score2')] == ''
        assert data[14][header.index('math_test_scores2')] == ''
    # #assertions for student who had partial test scores returned for first test
        assert float(data[15][header.index('id')])== 16
        assert data[15][header.index('language_test_scores')] == ''
        assert float(data[15][header.index('reading_test_score')]) == 88
        assert data[15][header.index('math_test_scores')] == ''
        assert float(data[15][header.index('total_points')])== 25
        assert data[15][header.index('matrix_languauge')] == ''
        assert data[15][header.index('matrix_math')] == ''
        assert float(data[15][header.index('matrix_reading')]) == 25
        assert data[15][header.index('matrix_languauge_retest')] == ''
        assert data[15][header.index('matrix_math_retest')] == ''
        assert data[15][header.index('matrix_reading_restest')] == ''
        assert data[15][header.index('total_points_retest')] == ''
        assert data[15][header.index('language_test_scores2')] == ''
        assert data[15][header.index('reading_test_score2')] == ''
        assert data[15][header.index('math_test_scores2')] == ''
        # #assertions for student who had partial test scores returned for retest
        assert float(data[16][header.index('id')])== 17
        assert float(data[16][header.index('language_test_scores')]) == 85
        assert float(data[16][header.index('reading_test_score')]) == 80
        assert float(data[16][header.index('math_test_scores')]) == 82
        assert float(data[16][header.index('total_points')])== 87
        assert float(data[16][header.index('matrix_languauge')]) == 23
        assert float(data[16][header.index('matrix_math')]) == 22
        assert float(data[16][header.index('matrix_reading')]) == 21
        assert data[16][header.index('matrix_languauge_retest')] == ''
        assert data[16][header.index('matrix_math_retest')] == ''
        assert data[16][header.index('matrix_reading_restest')] == ''
        assert float(data[16][header.index('total_points_retest')]) == 21
        assert data[16][header.index('language_test_scores2')] == ''
        assert data[16][header.index('reading_test_score2')] == ''
        assert data[16][header.index('math_test_scores2')] == ''
# #assertions for student who had partial test scores returned for first test
        assert float(data[17][header.index('id')])== 18
        assert float(data[17][header.index('language_test_scores')]) == 90
        assert float(data[17][header.index('reading_test_score')]) == 90
        assert data[17][header.index('math_test_scores')] == ''
        assert float(data[17][header.index('total_points')])== 52
        assert float(data[17][header.index('matrix_languauge')]) == 26
        assert data[17][header.index('matrix_math')] == ''
        assert float(data[17][header.index('matrix_reading')]) == 26
        assert data[17][header.index('matrix_languauge_retest')] == ''
        assert data[17][header.index('matrix_math_retest')] == ''
        assert data[17][header.index('matrix_reading_restest')] == ''
        assert data[17][header.index('total_points_retest')] == ''
        assert data[17][header.index('language_test_scores2')] == ''
        assert data[17][header.index('reading_test_score2')] == ''
        assert data[17][header.index('math_test_scores2')] == ''
# #assertions for student who had partial test scores returned for first test
        assert float(data[18][header.index('id')])== 19
        assert float(data[18][header.index('language_test_scores')]) == 90
        assert data[18][header.index('reading_test_score')] == ''
        assert float(data[18][header.index('math_test_scores')]) == 87
        assert float(data[18][header.index('total_points')])== 50
        assert float(data[18][header.index('matrix_languauge')]) == 26
        assert float(data[18][header.index('matrix_math')]) == 24
        assert data[18][header.index('matrix_reading')] == ''
        assert data[18][header.index('matrix_languauge_retest')] == ''
        assert data[18][header.index('matrix_math_retest')] == ''
        assert data[18][header.index('matrix_reading_restest')] == ''
        assert data[18][header.index('total_points_retest')] == ''
        assert data[18][header.index('language_test_scores2')] == ''
        assert data[18][header.index('reading_test_score2')] == ''
        assert data[18][header.index('math_test_scores2')] == ''
# #assertions for student who had partial test scores returned for retest
        assert float(data[19][header.index('id')])== 20
        assert float(data[19][header.index('language_test_scores')]) == 78
        assert float(data[19][header.index('reading_test_score')]) == 78
        assert float(data[19][header.index('math_test_scores')]) == 78
        assert float(data[19][header.index('total_points')])== 82
        assert float(data[19][header.index('matrix_languauge')]) == 20
        assert float(data[19][header.index('matrix_math')]) == 20
        assert float(data[19][header.index('matrix_reading')]) == 20
        assert data[19][header.index('matrix_languauge_retest')] == ''
        assert float(data[19][header.index('matrix_math_retest')]) == 24
        assert float(data[19][header.index('matrix_reading_restest')]) == 19
        assert float(data[19][header.index('total_points_retest')]) == 65
        assert data[19][header.index('language_test_scores2')] == ''
        assert float(data[19][header.index('reading_test_score2')]) == 77
        assert float(data[19][header.index('math_test_scores2')]) == 87





