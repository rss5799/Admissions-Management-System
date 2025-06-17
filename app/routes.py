from flask import Blueprint, render_template, request, session
import pandas as pd
import numpy as np
from app.models import student
import json

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
        assign_student_to_current_student_session(current_student)
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
        #update dataframe

        schoolMint_df= pd.read_csv('DummyDataComplete.csv')
        for index, row in schoolMint_df.iterrows():
            if str(row['id']) == str(current_student.id):
                gpa = calculate_gpa(grades)
                print(gpa)
                row['gpa'] = calculate_gpa(grades)
                print(row['id'], row['gpa'])
        
        current_student.gpa = gpa
        assign_student_to_current_student_session(current_student)
    return render_template('student_details.html', results = current_student)


def retrieve_current_student():
    #if youre coming from points inputs (student search page)
    if request.args.get('id_query'):
        current_id = request.args.get('id_query')
    #if you're coming from report card input page
    else:
        JSON_current_student= session.get('current_student')
        student_dict = json.loads(JSON_current_student)
        temp_current_student = student.Student(**student_dict)
        current_id = temp_current_student.id

    schoolMint_df = pd.read_csv('DummyDataComplete.csv')
    schoolMint_df['gpa'] = None
    schoolMint_df.to_csv('DummyDataComplete.csv', index=False)
    schoolMint_df['id'] = schoolMint_df['id'].astype(str)
    studentId = str(current_id)
    index = schoolMint_df.index[schoolMint_df['id']== studentId].tolist()
    if index:
        currentStudent = student.Student(
            id = current_id,
            gpa = schoolMint_df['gpa'].iloc[index[0]],
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
        return(currentStudent)
    else:
        print("ID not found")
        return(0)
    

    
def assign_student_to_current_student_session(current_student):
    #prepare dictionary for json
    #turn numpy nan to empty string
    current_student = turn_na_to_emptystring(current_student)
    #turn all attribute values to json serializable values
    current_student = prepare_for_json(current_student)
    #convert dictuarion to JSON data
    studentJSONdata = json.dumps(current_student)
    #pass JSON data to the other pages with a unique identifier
    session['current_student'] = studentJSONdata
    
def turn_na_to_emptystring(student):
        #replace all empty values with blank string
        for attr, value in vars(student).items():
            if isinstance(value, float) and np.isnan(value):
                setattr(student, attr, "")
        return student

def prepare_for_json(obj):
    new_dict = {}
    for key, value in obj.__dict__.items():
        if isinstance(value, np.ndarray):
            new_dict[key] = value.tolist()
        elif isinstance(value, np.integer):
          new_dict[key] = int(value)
        elif isinstance(value, np.floating):
          new_dict[key] = float(value)
        else:
            new_dict[key] = value
    return new_dict











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