from flask import Blueprint, render_template, request, session, flash, redirect, send_file, url_for
from app.utils.csv_reader_writer import fetch_updated_student_instance
from app.forms.report_card import ReportCardForm
from app.services.report_card_service import ReportCardService
import os
from app.services.details_of_test_days import retrieve_unique_test_dates, retrieve_test_day_counts
import csv
import pandas as pd
from app.utils.csv_riverside_writer import combine_data
from app.services.filtering import DataFilter
from app.services.sorting import apply_sorting


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
TEMP_ORIGINAL_SM_DATA = os.path.join(UPLOAD_FOLDER, 'original_schoolmint.csv')
schoolMint_csv = ('data/updated_schoolmint.csv')


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
@bp.route('/', methods={'GET', 'POST'})
def index():
    if request.method == 'POST':
        #TODO add logic to authenticate
        return render_template("landing.html", breadcrumbs=[{"title": "Landing", "url": url_for('main.landing')}])
    return render_template("home.html", breadcrumbs=[{"title": "Home", "url": url_for('main.index')}])

#logout page
@bp.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

#first page for all users
@bp.route("/landing")
def landing():
    return render_template("landing.html", breadcrumbs=[{"title": "Landing", "url": url_for('main.landing')}])

#navigation scren to all functionality
@bp.route("/menu")
def menu():
    return render_template("menu.html", breadcrumbs=[{"title": "Main Menu", "url": url_for('main.menu')}])

#search for student here (new points_inputs)
@bp.route("/point_inputs/")
def point_inputs():
    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Search Students", "url": url_for('main.point_inputs')}
    ]

    # New single line load csv and fill empties
    schoolmint_data = pd.read_csv('data/updated_schoolmint.csv').fillna('')

    # Handle filtering
    filter_field = request.args.get("filter_field")
    filter_value = request.args.get("filter_value")

    # Normalize filter_field to df cols
    if filter_field:
        match = [col for col in schoolmint_data.columns if col.lower() == filter_field.lower()]
        filter_field = match[0] if match else None

    # Apply filtering
    schoolmint_data, filter_values = DataFilter(schoolmint_data).apply(filter_field, filter_value)
   
    # Apply new reusable Sorting logic
    schoolmint_data = apply_sorting(schoolmint_data)

    # float -> int, except gpa
    for index, row in schoolmint_data.iterrows():
        for col_name, value in row.items():
            if(col_name != 'gpa' and isinstance(value, float)):
                value = int(value)
                schoolmint_data.loc[index, col_name] = value
    
    records = schoolmint_data.to_dict(orient='records')
    return render_template("point_inputs.html", 
                           breadcrumbs=breadcrumbs, 
                           headers = schoolmint_data.columns, 
                           records = records, 
                           filter_field=filter_field,
                           filter_values=filter_values
                           )

#search for a student here (old point_inputs)
'''
@bp.route("/point_inputs/")
def point_inputs():
    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Search Students", "url": url_for('main.point_inputs')}
    ]
    schoolmint_data = pd.read_csv('data/updated_schoolmint.csv')
    schoolmint_data = schoolmint_data.fillna('')

    sort_column = request.args.get('sort_by')
    sort_order = request.args.get('order', 'asc')

    if sort_column and sort_column in schoolmint_data.columns:
        schoolmint_data = schoolmint_data.sort_values(by=sort_column, ascending=(sort_order=='asc'))

    for index, row in schoolmint_data.iterrows():
        for col_name, value in row.items():
            if(col_name != 'gpa' and isinstance(value, float)):
                value = int(value)
                schoolmint_data.loc[index, col_name] = value
    
    records = schoolmint_data.to_dict(orient='records')
    return render_template("point_inputs.html", breadcrumbs=breadcrumbs, headers = schoolmint_data.columns, records = records)
'''

#see individual student deatils after search
@bp.route("/student_details/", methods = ['GET'])
def student_details():
    if os.path.exists('data/updated_schoolmint.csv'):
        current_student = retrieve_current_student()
        breadcrumbs = [
            {"title": "Main Menu", "url": url_for('main.menu')},
            {"title": "Search Students", "url": url_for('main.point_inputs')},
            {"title": f"Student {current_student.id}" if current_student else "Student Details", "url": url_for('main.student_details')}
        ]
        if current_student:
            session['current_id'] = current_student.id
            return render_template("student_details.html", results = current_student, breadcrumbs=breadcrumbs)
        else:
            flash("ID not found", 'noStudent')
            return redirect(url_for('main.point_inputs'))

    else:
        breadcrumbs = [
            {"title": "Main Menu", "url": url_for('main.menu')},
            {"title": "Search Students", "url": url_for('main.point_inputs')},
            {"title": f"Student Details", "url": url_for('main.student_details')}
        ]
        return render_template("point_inputs.html", results = "Please upload a SchoolMint Data File", breadcrumbs=breadcrumbs)


#enter/update report card grades
@bp.route("/enter_report_card/", methods = ['GET', 'POST'])
def enter_report_card():
    current_student = retrieve_current_student()
    form = ReportCardForm()

    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Search Students", "url": url_for('main.point_inputs')},
        {"title": "Student Details", "url": url_for('main.student_details')},
        {"title": "Enter Report Card", "url": url_for('main.enter_report_card')}
    ]

    if request.method == "POST":
        form_data = request.form.to_dict()
        print(form_data)
        service = ReportCardService(form_data, current_student)
        result = service.process()

        session["current_id"] = current_student.id

        return render_template(
            "enter_report_card.html",
            form=form,
            results=current_student,
            gpa=result["gpa"],
            matrix_gpa=result["matrix_gpa"],
            breadcrumbs=breadcrumbs
        )
    return render_template(
        "enter_report_card.html",
        form=form,
        results=current_student,
        breadcrumbs=breadcrumbs
    )

@bp.route("/upcoming_tests/", methods=['GET','POST'])
def upcoming_tests():
    upcoming_test_dates = retrieve_unique_test_dates(schoolMint_csv)
    test_day_numbers = None
    selected_test_date = ""

    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Upcoming Tests", "url": url_for('main.upcoming_tests')}
    ]

    if request.method == 'POST':        
        selected_test_date = request.form.get('upcoming_tests_dropdown')
        test_day_numbers = retrieve_test_day_counts(schoolMint_csv, selected_test_date)

    return render_template("upcoming_tests.html", dates = upcoming_test_dates, selected_test_date = selected_test_date, test_day_numbers = test_day_numbers, breadcrumbs=breadcrumbs)

@bp.route("/merge_riverside", methods=['GET','POST'])
def merge_riverside():
    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Merge Riverside File", "url": url_for('main.merge_riverside')}
    ]
    
    if request.method == 'GET':
        return render_template("merge_riverside.html", breadcrumbs=breadcrumbs)
    if request.method == 'POST':
        if 'riversidefile' not in request.files:
            flash("No file part")
            return render_template("merge_riverside.html", uploadresults = "Riverside Data File must be uploaded to proceed with merge.", breadcrumbs=breadcrumbs)

        riversidefile = request.files['riversidefile']

        if riversidefile.filename == '':
            flash("No selected file")
            return render_template("merge_riverside.html", uploadresults = "Riverside Data File must be uploaded to proceed with merge.", breadcrumbs=breadcrumbs)

        if riversidefile and riversidefile.filename.endswith('.csv'):
            request.files['riversidefile'].save('data/riverside.csv')
            combine_data(schoolMint_csv, 'data/riverside.csv')
            return render_template("menu.html", breadcrumbs=[{"title": "Main Menu", "url": url_for('main.menu')}])
        else:
            return render_template("merge_riverside.html", uploadresults = "Riverside Data File must be uploaded to proceed with merge.", breadcrumbs=breadcrumbs)

@bp.route("/exports/", methods = ["GET", "POST"])
def exports_page():
    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Exports", "url": url_for('main.exports_page')}
    ]
    return render_template("exports.html", breadcrumbs=breadcrumbs)

@bp.route("/export_csv", methods = ['POST'])
def export_csv():
    if request.method == "POST":
        schoolMintcsv = (f'{UPLOAD_FOLDER}/updated_schoolmint.csv')
        return send_file(schoolMintcsv, as_attachment=True)
    return render_template("menu.html", breadcrumbs=[{"title": "Main Menu", "url": url_for('main.menu')}])

@bp.route("/upload_csv", methods=["POST"])
def upload_schoolmint_csv():
    if 'schoolmintfile' not in request.files:
        flash("No file part")
        return render_template("landing.html", schoolMintresults = "Schoolmint Data File must be uploaded to continue", breadcrumbs=[{"title": "Landing", "url": url_for('main.landing')}])

    schoolmintfile = request.files['schoolmintfile']

    if schoolmintfile.filename == '':
        flash("No selected file")
        return render_template("landing.html", uploadresults = "Schoolmint Data File must be uploaded to continue", breadcrumbs=[{"title": "Landing", "url": url_for('main.landing')}])

    if schoolmintfile and schoolmintfile.filename.endswith('.csv'):
        schoolmintfile.save('data/original_schoolmint.csv')
        with open('data/original_schoolmint.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            with open(schoolMint_csv, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                for row in reader:
                    writer.writerow(row)
        return render_template("menu.html", breadcrumbs=[{"title": "Main Menu", "url": url_for('main.menu')}])
    else:
        return render_template("landing.html", uploadresults = "Invalid file type please upload a csv", breadcrumbs=[{"title": "Landing", "url": url_for('main.landing')}])

@bp.route("/unresponsive_students/")
def unresponsive_students():
    breadcrumbs = [
        {"title": "Main Menu", "url": url_for('main.menu')},
        {"title": "Unresponsive Students", "url": url_for('main.unresponsive_students')}
    ]
    return render_template("unresponsive_students.html", breadcrumbs=breadcrumbs)