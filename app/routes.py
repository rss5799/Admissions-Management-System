from flask import Blueprint, render_template, request, session, flash, redirect
import pandas as pd
import numpy as np
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance, write_gpa_to_csv


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
    else:
        return render_template("student_details.html", results = None)

@bp.route("/enter_report_card/", methods = ['GET', 'POST'])
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
    if current_student != 0:
        grades = {
            "english": "",
            "math": "",
            "science": "",
            "social_studies": "",
            "language": ""
        }
        gpa = None
        matrix_gpa = None

        if request.method == 'POST':
            grades['english'] = request.form['english']
            grades['math'] = request.form['math']
            grades['science'] = request.form['science']
            grades['social_studies'] = request.form['social_studies']
            grades['language'] = request.form['language']

            from app.services.matrix_calculator import calculate_gpa, lookup_matrix_points, matrix

            gpa = calculate_gpa(grades)
            matrix_gpa = lookup_matrix_points(gpa, matrix["gpa"]) # gpa->matrix_gpa value in DummyDataComplete.csv

            #update csv
            write_gpa_to_csv(current_student.id, gpa, matrix_gpa)
            #retrieve updated student data with new report card info
            current_student = retrieve_current_student()
            if current_student is not None:
                flash("GPA and Matrix GPA Score successfully calculated.")
                #set session
                session['current_id'] = current_student.id
                return render_template('enter_report_card.html', results = current_student, grades = grades, gpa = gpa, matrix_gpa = matrix_gpa)
            else:
                return render_template('enter_report_card.html', results = None, grades = None, gpa = None, matrix_gpa = None)
    else:
        return render_template('enter_report_card.html', results = None, grades = None, gpa = None, matrix_gpa = None)
    
def retrieve_current_student():
    #if youre coming from student search page
    if request.args.get('id_query'):
        current_id = request.args.get('id_query')
        if fetch_updated_student_instance(current_id):
            current_student = fetch_updated_student_instance(current_id)
            if current_student:
                return(current_student)
            else:
                print("ID not found")
                return(0)
        else:
            print("ID not found")
            return(0)
    #if you're coming from report card input page
    else:
        current_id= session.get('current_id')
        if current_id:
            current_student = fetch_updated_student_instance(current_id)
            return(current_student)
        else:
            print("No student ID Found")
            return(0)





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




















@bp.route("/export_csv")
def export_csv():
        



        return redirect("/exports")