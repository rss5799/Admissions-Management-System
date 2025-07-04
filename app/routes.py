from flask import Blueprint, render_template, request, session, flash, redirect
from app.utils.csv_reader_writer import fetch_updated_student_instance
from app.forms.report_card import ReportCardForm
from app.services.report_card_service import ReportCardService
import os
from flask import send_file, url_for
from app.services.details_of_test_days import retrieve_unique_test_dates, retrieve_test_day_counts
import pyrebase
import csv
from app.utils.csv_riverside_writer import combine_data

config = {
    'apiKey': "AIzaSyDObAkxu03wa769hSlSaYkGb27Z1SJ95Fg",
    'authDomain': "admissionsmanagementsystem.firebaseapp.com",
    'projectId': "admissionsmanagementsystem",
    'storageBucket': "admissionsmanagementsystem.firebasestorage.app",
    'messagingSenderId': "178704031743",
    'appId': "1:178704031743:web:f0773e4dfa6702049711ca",
    'databaseURL' : '' 
}

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
TEMP_ORIGINAL_SM_DATA = os.path.join(UPLOAD_FOLDER, 'original_schoolmint.csv')
schoolMint_csv = ('data/updated_schoolmint.csv')



# schoolMint_original_csv = os.path.join(UPLOAD_FOLDER, 'DummyDataComplete.csv')
# updated_df = os.path.join(UPLOAD_FOLDER, 'updated_student_data.csv')
# CSV_DIR = "csv_files"
# os.makedirs(CSV_DIR, exist_ok=True)

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
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return render_template("landing.html")
        except:
            return render_template("home.html", results = "Invalid Login, please try again")
    
    return render_template("home.html")

#logout page
@bp.route('/logout')
def logout():
    pass

#first page for all users
@bp.route("/landing")
def landing():
    return render_template("landing.html")

#navigation scren to all functionality
@bp.route("/menu")
def menu():
    return render_template("menu.html")

#search for a student here
@bp.route("/point_inputs/")
def point_inputs():
    return render_template("point_inputs.html")

#see individual student deatils after search
@bp.route("/student_details/", methods = ['GET'])
def student_details():
    current_student = retrieve_current_student()

    if current_student:
        session['current_id'] = current_student.id
        return render_template("student_details.html", results = current_student)
    else:
        return render_template("point_inputs.html", results = "No records for student")

#enter/update report card grades
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

@bp.route("/upcoming_tests/", methods=['GET','POST'])
def upcoming_tests():
    upcoming_test_dates = retrieve_unique_test_dates(schoolMint_csv)
    test_day_numbers = None
    selected_test_date = ""

    if request.method == 'POST':        
        selected_test_date = request.form.get('upcoming_tests_dropdown')
        test_day_numbers = retrieve_test_day_counts(schoolMint_csv, selected_test_date)
    
    return render_template("upcoming_tests.html", dates = upcoming_test_dates, selected_test_date = selected_test_date, test_day_numbers = test_day_numbers)

@bp.route("/merge_riverside", methods=['GET','POST'])
def merge_riverside():
    if request.method == 'GET':
        return render_template("merge_riverside.html")
    if request.method == 'POST':
        if 'riversidefile' not in request.files:
            flash("No file part")
            return render_template("merge_riversdie.html", uploadresults = "Riverside Data File must be uploaded to proceed with merge.")

        riversidefile = request.files['riversidefile']

        if riversidefile.filename == '':
            flash("No selected file")
            return render_template("merge_riversdie.html", uploadtresults = "Riverside Data File must be uploaded to proceed with merge.")

        if riversidefile and riversidefile.filename.endswith('.csv'):
                request.files['riversidefile'].save('data/riverside.csv')
                combine_data(schoolMint_csv, 'data/riverside.csv')
                return render_template("menu.html")
        else:
            return render_template("merge_riversdie.html", uploadtresults = "Riverside Data File must be uploaded to proceed with merge.")

#placeholder routes to be developed
@bp.route("/exports/")
def exports_page():
    return render_template("exports.html")

@bp.route("/export_csv")
def export_csv():
    if os.path.exists(schoolMint_csv):
        return send_file(schoolMint_csv, as_attachment=True)
    else:
        flash("CSV file not found.")
        return redirect(url_for('main.exports_page'))

@bp.route("/upload_csv", methods=["POST"])
def upload_schoolmint_csv():
    if 'schoolmintfile' not in request.files:
        flash("No file part")
        return render_template("landing.html", schoolMintresults = "Schoolmint Data File must be uploaded to continue")

    schoolmintfile = request.files['schoolmintfile']

    if schoolmintfile.filename == '':
        flash("No selected file")
        return render_template("landing.html", uploadresults = "Schoolmint Data File must be uploaded to continue")

    if schoolmintfile and schoolmintfile.filename.endswith('.csv'):
        schoolmintfile.save('data/original_schoolmint.csv')
        with open('data/original_schoolmint.csv', 'r', newline='') as infile:
            reader = csv.reader(infile)
            with open(schoolMint_csv, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                for row in reader:
                    writer.writerow(row)
        return render_template("menu.html")
    else:
        return render_template("landing.html", uploadresults = "Invalid file type please upload a csv")


@bp.route("/unresponsive_students/")
def unresponsive_students():
    return render_template("unresponsive_students.html")