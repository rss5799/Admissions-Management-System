from flask import Blueprint, render_template, request, session
import pandas as pd
import numpy as np
from app.models import student
import json
from app.csv_utils.csv_reader import fetch_updated_student_instance

bp = Blueprint('main', __name__)



#starting point for the app
@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/point_inputs/")
def point_inputs():
    return render_template("point_inputs.html")

@bp.route("/student_details/", methods = ['GET'])
def student_details():
    current_student = retrieve_current_student()
    if current_student:
        #assign session['current_student'] to current_student
        session['current_id'] = current_student.id
        return render_template("student_details.html", results = current_student)

@bp.route("/enter_report_card/")
def enter_report_card():
    current_student = retrieve_current_student()
        # Provide default empty grades so template doesn't crash
    grades = {
        "english": "",
        "math": "",
        "science": "",
        "social_studies": "",
        "language": ""
    }
    
    return render_template("enter_report_card.html", results = current_student, grades=grades)

@bp.route('/calculate_gpa', methods=['GET', 'POST'])
def calculate_gpa_route():
    current_student = retrieve_current_student()
    grades = {
        "english": "",
        "math": "",
        "science": "",
        "social_studies": "",
        "language": ""
    }
    gpa = None

    if request.method == 'POST':
        grades['english'] = request.form['english']
        grades['math'] = request.form['math']
        grades['science'] = request.form['science']
        grades['social_studies'] = request.form['social_studies']
        grades['language'] = request.form['language']

        from app.services.matrix_calculator import calculate_gpa
        gpa = calculate_gpa(grades)
        #update dataframe
    return render_template('student_details.html', results = current_student)


def retrieve_current_student():
    #if youre coming from points inputs (student search page)
    if request.args.get('id_query'):
        current_id = request.args.get('id_query')
        if fetch_updated_student_instance(current_id):
            current_student = fetch_updated_student_instance(current_id)
            return(current_student)
        else:
            print("ID not found")
            return(0)
    #if you're coming from report card input page
    else:
        current_id= session.get('current_id')
        current_student = fetch_updated_student_instance(current_id)
        return(current_student)
    
 











#placeholder routes to be developed
@bp.route("/exports/")
def exports():
    return render_template("exports.html")

@bp.route("/upcoming_tests/")
def upcoming_tests():
    return render_template("upcoming_tests.html")

@bp.route("/unresponsive_students/")
def unresponsive_students():
    return render_template("unresponsive_students.html")