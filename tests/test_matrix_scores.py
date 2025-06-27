import pytest
from flask import render_template
import random
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance, write_gpa_to_csv
from app import create_app
from app.services.matrix_calculator import lookup_matrix_points, matrix, calculate_gpa, calculate_total_matrix
import json

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

