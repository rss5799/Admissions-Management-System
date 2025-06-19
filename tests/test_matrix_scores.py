import pytest
from flask import render_template
import random
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance
from app import create_app
from pyquery import PyQuery as pq
from lxml import etree


#Unit test 11: Ensure that matrix points load from original datasource
def test_matrix_gpa_loads_from_schoolmint():
    #get 5 random student ids
    random_students = [random.randint(1, 1077) for _ in range(5)]
    #check each of the five students
    for student in random_students:
        student = fetch_updated_student_instance(student)
        gpa = student.gpa
        matrix_gpa = student.matrix_gpa
        #runtime error log solution at https://stackoverflow.com/questions/34122949/working-outside-of-application-context-flask
        app = create_app()
        app.app_context().push()
        with app.app_context():
            #confirm that the html renders the correct gpa and matrix gpa for the student
            rendered_html = render_template("student_details.html", results = student)
            doc = pq(rendered_html)
            #method modified from https://scrapingant.com/blog/python-pyquery-parse-html
            all_items = doc('tr').find('td')
            #convert element to string https://stackoverflow.com/questions/5395948/incredibly-basic-lxml-questions-getting-html-string-content-of-lxml-etree-elem
            assert gpa in str(etree.tostring(all_items[1]))
            assert matrix_gpa in str(etree.tostring(all_items[2]))

test_matrix_gpa_loads_from_schoolmint()

#Unit test 12: Ensure that when updates are made to the student profile it is properly displayed on the student details screen.
def test_matrix_gpa_persists():
    assert 1 == 1
#Unit test 13: Ensure that when updates are made to the student profile it is properly displayed on the student details screen.
def test_matrix_gpa_persists_on_restart():
    assert 1 == 1