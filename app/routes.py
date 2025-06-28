from flask import Blueprint, render_template, request, session, flash, redirect
import pandas as pd
import numpy as np
from app.csv_utils.csv_reader_writer import fetch_updated_student_instance, write_gpa_to_csv
from app.forms.report_card import ReportCardForm
from app.services.report_card_service import ReportCardService
import os
from flask import send_file, url_for

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
UPDATED_FILE = os.path.join(UPLOAD_FOLDER, 'updated_student_data.csv')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

schoolMint_df = os.path.join(UPLOAD_FOLDER, 'DummyDataComplete.csv')
updated_df = os.path.join(UPLOAD_FOLDER, 'updated_student_data.csv')
CSV_DIR = "csv_files"
os.makedirs(CSV_DIR, exist_ok=True)

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
    return render_template("landing.html")

@bp.route("/menu")
def menu():
    return render_template("menu.html")

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
def exports_page():
    return render_template("exports.html")

@bp.route("/export_csv")
def export_csv():
    if os.path.exists(UPDATED_FILE):
        return send_file(UPDATED_FILE, as_attachment=True)
    else:
        flash("CSV file not found.")
        return redirect(url_for('main.exports_page'))

@bp.route("/upload_csv", methods=["POST"])
def upload_csv():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(url_for('main.exports_page'))

    file = request.files['file']

    if file.filename == '':
        flash("No selected file")
        return redirect(url_for('main.exports_page'))

    if file and file.filename.endswith('.csv'):
        file.save(UPDATED_FILE)  
        flash("CSV uploaded and overwritten successfully.")
    else:
        flash("Invalid file type. Please upload a CSV.")

    return redirect(url_for('main.exports_page'))

#placeholder routes to be developed


@bp.route("/upcoming_tests/")
def upcoming_tests():
    return render_template("upcoming_tests.html")

@bp.route("/unresponsive_students/")
def unresponsive_students():
    return render_template("unresponsive_students.html")