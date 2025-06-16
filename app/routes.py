from flask import Blueprint, render_template, request, session
import pandas as pd
import numpy as np
from app.models import student
import json

schoolMint_df = pd.read_csv('DummyDataComplete.csv')


# class Student:
#     def __init__(self, id, gpa, matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, matrix_points_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up, current_school):
#         self.id = id
#         self.gpa = gpa
#         self.matrix_gpa = matrix_gpa
#         self.language_test_scores = language_test_scores
#         self.reading_test_score = reading_test_score
#         self.math_test_scores = math_test_scores
#         self.total_points=total_points
#         self.matrix_languauge = matrix_languauge
#         self.matrix_math = matrix_math
#         self.matrix_reading = matrix_reading
#         self.matrix_points_total = matrix_points_total
#         self.status = status
#         self.matrix_languauge_retest = matrix_languauge_retest
#         self.matrix_math_retest = matrix_math_retest
#         self.matrix_reading_restest = matrix_reading_restest
#         self.total_points_retest = total_points_retest
#         self.updated_at = updated_at
#         self.guardian1_email = guardian1_email
#         self.guardian2_email = guardian2_email
#         self.grade = grade
#         self.deliver_test_accomodation_approved = deliver_test_accomodation_approved
#         self.test_date_sign_up = test_date_sign_up
#         self.current_school = current_school


bp = Blueprint('main', __name__)


# Use the relative path to the credentials file won't need this for new csv import method
# key_path = os.path.join(os.path.dirname(__file__), "/Users/taracan/Documents/SWENG894/Admissions-Management-System/credentials/firebase_key.json")
# cred = credentials.Certificate(key_path)
# firebase_admin.initialize_app(cred)

@bp.route('/calculate_gpa', methods=['GET', 'POST'])
def calculate_gpa_route():
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

    return render_template('enter_report_card.html', gpa=gpa, grades=grades)



@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/exports/")
def exports():
    return render_template("exports.html")

@bp.route("/point_inputs/")
def point_inputs():
    return render_template("point_inputs.html")


@bp.route("/upcoming_tests/")
def upcoming_tests():
    return render_template("upcoming_tests.html")

@bp.route("/unresponsive_students/")
def unresponsive_students():
    return render_template("unresponsive_students.html")

@bp.route("/student_details/", methods=['GET'])
def student_details():
    current_id_query_result = request.args.get('id_query')
    current_student = perform_student_search(current_id_query_result)
    if current_student:
        current_student = turn_na_to_emptystring(current_student)
        studentJSONdata = json.dumps(current_student.toJson())
        #prepare id and grade to be passed to other pages   
        # session['current_student'] = studentJSONdata
        # grade = str(current_student.grade)
        # session['current_student_grade'] = grade
        return render_template("student_details.html", results = current_student, query = current_id_query_result)
    else:
        return render_template("point_inputs.html", results = "Student Not Found", query = current_id_query_result)
    
@bp.route("/enter_report_card/")
def enter_report_card():
    current_student_id = session.get('current_student_id')
    current_student_grade = session.get('current_student_grade')

    # Provide default empty grades so template doesn't crash
    grades = {
        "english": "",
        "math": "",
        "science": "",
        "social_studies": "",
        "language": ""
    }

    return render_template("/enter_report_card.html", 
                            current_student_id=current_student_id, 
                            current_student_grade=current_student_grade,
                            grades=grades)

def perform_student_search(query):
       schoolMint_df['id'] = schoolMint_df['id'].astype(str)
       studentId = str(query)
       index = schoolMint_df.index[schoolMint_df['id']== studentId].tolist()
       if index:
            currentStudent = student.Student(
                id = query,
                gpa = "", #pull from student class after calculated
                matrix_gpa = schoolMint_df['matrix_gpa'].iloc[index[0]],
                language_test_scores = schoolMint_df['language_test_scores'].iloc[index[0]],
                reading_test_score = schoolMint_df['reading_test_score'].iloc[index[0]], 
                math_test_scores =  schoolMint_df['math_test_scores'].iloc[index[0]],
                total_points = schoolMint_df['total_points'].iloc[index[0]],
                matrix_languauge = schoolMint_df['matrix_languauge'].iloc[index[0]], 
                matrix_math = schoolMint_df['matrix_math'].iloc[index[0]],
                matrix_reading = schoolMint_df['matrix_reading'].iloc[index[0]],
                matrix_points_total= schoolMint_df['matrix_languauge'].iloc[index[0]] + schoolMint_df['matrix_math'].iloc[index[0]]+ schoolMint_df['matrix_reading'].iloc[index[0]] + schoolMint_df['matrix_gpa'].iloc[index[0]] ,
                status = schoolMint_df['status'].iloc[index[0]],
                matrix_languauge_retest = schoolMint_df['matrix_languauge_retest'].iloc[index[0]],
                matrix_math_retest = schoolMint_df['matrix_math_retest'].iloc[index[0]],
                matrix_reading_restest = schoolMint_df['matrix_reading_restest'].iloc[index[0]],
                total_points_retest = schoolMint_df['total_points_retest'].iloc[index[0]],
                updated_at = schoolMint_df['updated_at'].iloc[index[0]],
                guardian1_email = schoolMint_df['guardian1_email'].iloc[index[0]],
                guardian2_email = schoolMint_df['guardian2_email'].iloc[index[0]],
                grade = schoolMint_df['grade'].iloc[index[0]],
                deliver_test_accomodation_approved = schoolMint_df['deliver_test_accomodation_approved'].iloc[index[0]],
                test_date_sign_up = schoolMint_df['test_date_sign_up'].iloc[index[0]],
                current_school = schoolMint_df['current_school'].iloc[index[0]]

            )
            print(currentStudent.matrix_gpa)
            return(currentStudent)
       else:
            print("ID not found")
            return(0)

def turn_na_to_emptystring(student):
        #replace all empty values with blank string
        for attr, value in vars(student).items():
            if isinstance(value, float) and np.isnan(value):
                setattr(student, attr, "")
        return student




