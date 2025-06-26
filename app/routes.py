from flask import Blueprint, render_template, request, session, flash, redirect
import pandas as pd
import numpy as np
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance, write_gpa_to_csv
from app.forms.report_card import ReportCardForm
from app.services.report_card_service import ReportCardService


bp = Blueprint('main', __name__)

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
        session['current_id'] = current_student.id
        return render_template("student_details.html", results = current_student)
    else:
        return render_template("student_details.html", results = None)

@bp.route("/enter_report_card/", methods = ['GET', 'POST'])
def enter_report_card():
    current_student = retrieve_current_student()
    form = ReportCardForm()

    if form.validate_on_submit():
        service = ReportCardService(form, current_student)
        result = service.process()

        session["current_id"] = current_student.id

        return render_template(
            "enter_report_card.html",
            form=form,
            results=current_student,
            gpa=result["gpa"],
            matrix_gpa=result["matrix_gpa"]
        )
    return render_template(
        "enter_report_card.html",
        form=form,
        results=current_student
    )

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