from flask import Blueprint, render_template, request, session
from firebase_admin import credentials, firestore, auth
import firebase_admin
import os

bp = Blueprint('main', __name__)


# Use the relative path to the credentials file
key_path = os.path.join(os.path.dirname(__file__), "/Users/taracan/Documents/SWENG894/Admissions-Management-System/credentials/firebase_key.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)


class Student:
    def __init__(self, id,matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, admission_test_score_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up):
        self.id = id
        self.matrix_gpa = matrix_gpa
        self.language_test_scores = language_test_scores
        self.reading_test_score = reading_test_score
        self.math_test_scores = math_test_scores
        self.total_points=total_points
        self.matrix_language = matrix_languauge
        self.matrix_math = matrix_math
        self.matrix_reading = matrix_reading
        self.admission_test_score_total = admission_test_score_total
        self.status = status
        self.matrix_language_retest = matrix_languauge_retest
        self.matrix_math_retest = matrix_math_retest
        self.matrix_reading_retest = matrix_reading_restest
        self.total_points_retest = total_points_retest
        self.updated_at = updated_at
        self.guardian1_email = guardian1_email
        self.guardian2_email = guardian2_email
        self.grade = grade
        self.deliver_test_accomodation_approved = deliver_test_accomodation_approved
        self.test_date_sign_up = test_date_sign_up



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
    results = perform_student_search(current_id_query_result)
    session['current_student_id'] = results.id
    session['current_student_grade'] = results.grade
    if results:
        return render_template("student_details.html", results = results, query = current_id_query_result)
    else:
        return render_template("point_inputs.html", results = "Student Not Found", query = current_id_query_result)
    
@bp.route("/enter_report_card/", methods=['GET'])
def enter_report_card():
    current_student_id = session.get('current_student_id')
    current_student_grade = session.get('current_student_grade')
    return render_template("/enter_report_card.html", current_student_id = current_student_id, current_student_grade = current_student_grade)


def perform_student_search(query):
    # Access Firestore
    db = firestore.client()
    collection_ref = db.collection('studentObject')
    docs = collection_ref.stream()
    print(docs)
    for doc in docs:      
        doc_data = doc.to_dict()
        for id in [str(doc_data['id'])]:
            if query == id:
                id = str(doc_data['id'])
                matrix_gpa = str(doc_data['matrix_gpa'])
                language_test_scores = str(doc_data['language_test_scores'])
                reading_test_score = str(doc_data['reading_test_score'])
                math_test_scores = str(doc_data['math_test_scores'])
                total_points = str(doc_data['total_points'])
                matrix_languauge = str(doc_data['matrix_languauge'])
                matrix_math = str(doc_data['matrix_math'])
                matrix_reading = str(doc_data['matrix_reading'])
                admission_test_score_total = (doc_data['matrix_languauge'] + doc_data['matrix_math'] + doc_data['matrix_reading'])
                status = str(doc_data['status'])
                matrix_languauge_retest = str(doc_data['matrix_languauge_retest'])
                matrix_math_retest = str(doc_data['matrix_math_retest'])
                matrix_reading_restest = str(doc_data['matrix_reading_restest'])
                total_points_retest = str(doc_data['total_points_retest'])
                updated_at = str(doc_data['updated_at'])
                guardian1_email = str(doc_data['guardian1_email'])
                guardian2_email = str(doc_data['guardian2_email'])
                grade = str(doc_data['grade'])
                deliver_test_accomodation_approved = str(doc_data['deliver_test_accomodation_approved'])
                test_date_sign_up = str(doc_data['test_date_sign_up'])
                current_student = Student(id, matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading,admission_test_score_total, status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up)
                return(current_student)
        

