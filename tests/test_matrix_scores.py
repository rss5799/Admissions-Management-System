import pytest
from flask import render_template
import random
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance, write_gpa_to_csv
from app import create_app
from pyquery import PyQuery as pq
from lxml import etree
from app.services.matrix_calculator import lookup_matrix_points, matrix, calculate_gpa, calculate_total_matrix


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
        print("SUCCESS")




#System Test 16: Ensure that matrix points load from original datasource
def test_matrix_gpa_loads_from_schoolmint():
    #get 5 random student ids
    random_students = [random.randint(1, 1077) for _ in range(5)]
    #check each of the five students
    counter = 0
    for student in random_students:
        student = fetch_updated_student_instance(student)
        #runtime error log solution at https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
        app = create_app()
        app.app_context().push()
        with app.app_context():
            #render the htmal
            rendered_html = render_template("student_details.html", results = student)
            #store the rendered html with pyquery
            doc = pq(rendered_html)
            #colect the list items (method modified from https://scrapingant.com/blog/python-pyquery-parse-html)
            all_items = doc('tr').find('td')
            #store the collected items in a list
            collect_contents = []
            for item in all_items:
                #convert element to string https://stackoverflow.com/questions/5395948/incredibly-basic-lxml-questions-getting-html-string-content-of-lxml-etree-elem
                collect_contents.append(str(etree.tostring(item)))
            
            #make the list a long string
            html_string = "".join(collect_contents)
            #store the unique substring that needs to be on the html
            substring = "GPA Points</td>\\n    'b'<td> " + student.gpa + "</td>\\n" + "    'b'<td>" + student.matrix_gpa
            if(student.gpa != ""):
                assert substring in html_string
                counter = counter + 1
    #it's probably good to ensure that you're testing at least one student (at least one of the five randoms has a stored gpa)
    if(counter == 0):
        test_matrix_gpa_loads_from_schoolmint()



#System test 17: Ensure that when updates are made to the student profile it is properly displayed on the student details screen.
def test_matrix_gpa_persists():
    #get 5 random student ids
    random_students = [random.randint(1, 1077) for _ in range(5)]
    #check each of the five students
    counter = 0
    for student in random_students:
        student = fetch_updated_student_instance(student)
        new_gpa = random.uniform(0.1, 4)
        while new_gpa == student.gpa:
            new_gpa = random.uniform(0.1, 4)
        
        new_matrix_gpa = lookup_matrix_points(new_gpa, matrix["gpa"]) # gpa->matrix_gpa value in DummyDataComplete.csv
        write_gpa_to_csv(student, new_gpa, new_matrix_gpa)
        
        
        #runtime error log solution at https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
        app = create_app()
        app.app_context().push()
        with app.app_context():
            #render the htmal
            rendered_html = render_template("student_details.html", results = student)
            #store the rendered html with pyquery
            doc = pq(rendered_html)
            #colect the list items (method modified from https://scrapingant.com/blog/python-pyquery-parse-html)
            all_items = doc('tr').find('td')
            #store the collected items in a list
            collect_contents = []
            for item in all_items:
                #convert element to string https://stackoverflow.com/questions/5395948/incredibly-basic-lxml-questions-getting-html-string-content-of-lxml-etree-elem
                collect_contents.append(str(etree.tostring(item)))
            
            #make the list a long string
            html_string = "".join(collect_contents)
            #store the unique substring that needs to be on the html
            substring = "GPA Points</td>\\n    'b'<td> " + student.gpa + "</td>\\n" + "    'b'<td>" + student.matrix_gpa
            if(student.gpa != ""):
                assert substring in html_string
                counter = counter + 1
    #it's probably good to ensure that you're testing at least one student (at least one of the five randoms has a stored gpa)
    if(counter == 0):
        test_matrix_gpa_persists()

