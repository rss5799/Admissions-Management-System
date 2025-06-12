from flask import Blueprint, render_template, request, session
import pandas as pd
from pathlib import Path

current_dir = Path(__file__).parent
student_df  = current_dir / 'DummyDataComplete.csv'

class Student:
    def __init__(self, id,matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, admission_test_score_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up):
        self.id = id
        self.matrix_gpa = matrix_gpa
        self.language_test_scores = language_test_scores
        self.reading_test_score = reading_test_score
        self.math_test_scores = math_test_scores
        self.total_points=total_points
        self.matrix_languauge = matrix_languauge
        self.matrix_math = matrix_math
        self.matrix_reading = matrix_reading
        self.admission_test_score_total = admission_test_score_total
        self.status = status
        self.matrix_languauge_retest = matrix_languauge_retest
        self.matrix_math_retest = matrix_math_retest
        self.matrix_reading_restest = matrix_reading_restest
        self.total_points_retest = total_points_retest
        self.updated_at = updated_at
        self.guardian1_email = guardian1_email
        self.guardian2_email = guardian2_email
        self.grade = grade
        self.deliver_test_accomodation_approved = deliver_test_accomodation_approved
        self.test_date_sign_up = test_date_sign_up


bp = Blueprint('main', __name__)


# Use the relative path to the credentials file won't need this for new csv import method
# key_path = os.path.join(os.path.dirname(__file__), "/Users/taracan/Documents/SWENG894/Admissions-Management-System/credentials/firebase_key.json")
# cred = credentials.Certificate(key_path)
# firebase_admin.initialize_app(cred)

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
        session['current_student_id'] = current_id_query_result
        grade = str(current_student.grade)
        session['current_student_grade'] = grade
        return render_template("student_details.html", results = current_student, query = current_id_query_result)
    else:
        return render_template("point_inputs.html", results = "Student Not Found", query = current_id_query_result)
    
@bp.route("/enter_report_card/")
def enter_report_card():
    current_student_id = session.get('current_student_id')
    current_student_grade = session.get('current_student_grade')
    #add logic for drowpdown listener
    return render_template("/enter_report_card.html", current_student_id = current_student_id, current_student_grade = current_student_grade)


def perform_student_search(query):
       student_df['id'] = student_df['id'].astype(str)
       studentId = str(query)
       index = student_df.index[student_df['id']== studentId].tolist()
       if index:
            currentStudent = Student(
                id = query,
                matrix_gpa = student_df['matrix_gpa'].iloc[index[0]],
                language_test_scores = student_df['language_test_scores'].iloc[index[0]],
                reading_test_score = student_df['reading_test_score'].iloc[index[0]], 
                math_test_scores =  student_df['math_test_scores'].iloc[index[0]],
                total_points = student_df['total_points'].iloc[index[0]],
                matrix_languauge = student_df['matrix_languauge'].iloc[index[0]], 
                matrix_math = student_df['matrix_math'].iloc[index[0]],
                matrix_reading = student_df['matrix_reading'].iloc[index[0]],
                admission_test_score_total = student_df['matrix_languauge'].iloc[index[0]] + student_df['matrix_math'].iloc[index[0]]+ student_df['matrix_reading'].iloc[index[0]],
                status = student_df['status'].iloc[index[0]],
                matrix_languauge_retest = student_df['matrix_languauge_retest'].iloc[index[0]],
                matrix_math_retest = student_df['matrix_math_retest'].iloc[index[0]],
                matrix_reading_restest = student_df['matrix_reading_restest'].iloc[index[0]],
                total_points_retest = student_df['total_points_retest'].iloc[index[0]],
                updated_at = student_df['updated_at'].iloc[index[0]],
                guardian1_email = student_df['guardian1_email'].iloc[index[0]],
                guardian2_email = student_df['guardian2_email'].iloc[index[0]],
                grade = student_df['grade'].iloc[index[0]],
                deliver_test_accomodation_approved = student_df['deliver_test_accomodation_approved'].iloc[index[0]],
                test_date_sign_up = student_df['test_date_sign_up'].iloc[index[0]]

            )
            print(currentStudent.matrix_gpa)
            return(currentStudent)
       else:
            print("ID not found")
            return




            # currentStudent = Student(
            # id = studentID,
            # matrix_gpa = row['matrix_gpa'],
            # language_test_scores = row['language_test_scores'],
            # reading_test_score = row['reading_test_score'], 
            # math_test_scores =  row['math_test_scores'],
            # total_points = row['total_points'],
            # matrix_languauge = row['matrix_languauge'], 
            # matrix_math = row['matrix_math'],
            # matrix_reading = row['matrix_reading'],
            # admission_test_score_total = row['matrix_languauge'] + row['matrix_math']+ row['matrix_reading'],
            # status = row['status'],
            # matrix_languauge_retest = row['matrix_languauge_retest'],
            # matrix_math_retest = row['matrix_math_retest'],
            # matrix_reading_restest = row['matrix_reading_restest'],
            # total_points_retest = row['total_points_retest'],
            # updated_at = row['updated_at'],
            # guardian1_email = row['guardian1_email'],
            # guardian2_email = row['guardian2_email'],
            # grade = row['grade'],
            # deliver_test_accomodation_approved = row['deliver_test_accomodation_approved'],
            # test_date_sign_up = row['test_date_sign_up']
            # )
            #return currentStudent







    # for student in student_df:
    #     if student.id == query:
    #         currentStudent = Student(
    #         id = student.id,
    #         matrix_gpa = student.matrix_gpa,
    #         language_test_scores = student.language_test_scores,
    #         reading_test_score = student.reading_test_score,
    #         math_test_scores = student.math_test_scores,
    #         total_points = student.total_points,
    #         matrix_language = student.matrix_languauge,
    #         matrix_math = student.matrix_math,
    #         matrix_reading = student.matrix_reading,
    #         admission_test_score_total = student.admission_test_score_total,
    #         status = student.status,
    #         matrix_language_retest = student.matrix_languauge_retest,
    #         matrix_math_retest = student.matrix_math_retest,
    #         matrix_reading_retest = student.matrix_reading_restest,
    #         total_points_retest = student.total_points_retest,
    #         updated_at = student.updated_at,
    #         guardian1_email = student.guardian1_email,
    #         guardian2_email = student.guardian2_email,
    #         grade = student.grade,
    #         deliver_test_accomodation_approved = student.deliver_test_accomodation_approved,
    #         test_date_sign_up = student.test_date_sign_up

    #         )
    #         return currentStudent

    # # Access Firestore
    # db = firestore.client()
    # collection_ref = db.collection('studentObject')
    # docs = collection_ref.stream()
    # print(docs)
    # for doc in docs:      
    #     doc_data = doc.to_dict()
    #     for id in [str(doc_data['id'])]:
    #         if query == id:
    #             id = str(doc_data['id'])
    #             matrix_gpa = str(doc_data['matrix_gpa'])
    #             language_test_scores = str(doc_data['language_test_scores'])
    #             reading_test_score = str(doc_data['reading_test_score'])
    #             math_test_scores = str(doc_data['math_test_scores'])
    #             total_points = str(doc_data['total_points'])
    #             matrix_languauge = str(doc_data['matrix_languauge'])
    #             matrix_math = str(doc_data['matrix_math'])
    #             matrix_reading = str(doc_data['matrix_reading'])
    #             admission_test_score_total = (doc_data['matrix_languauge'] + doc_data['matrix_math'] + doc_data['matrix_reading'])
    #             status = str(doc_data['status'])
    #             matrix_languauge_retest = str(doc_data['matrix_languauge_retest'])
    #             matrix_math_retest = str(doc_data['matrix_math_retest'])
    #             matrix_reading_restest = str(doc_data['matrix_reading_restest'])
    #             total_points_retest = str(doc_data['total_points_retest'])
    #             updated_at = str(doc_data['updated_at'])
    #             guardian1_email = str(doc_data['guardian1_email'])
    #             guardian2_email = str(doc_data['guardian2_email'])
    #             grade = str(doc_data['grade'])
    #             deliver_test_accomodation_approved = str(doc_data['deliver_test_accomodation_approved'])
    #             test_date_sign_up = str(doc_data['test_date_sign_up'])
    #             current_student = Student(id, matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading,admission_test_score_total, status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up)
    #             return(current_student)
        

class Student:
    def __init__(self, id,matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, admission_test_score_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up):
        self.id = id
        self.matrix_gpa = matrix_gpa
        self.language_test_scores = language_test_scores
        self.reading_test_score = reading_test_score
        self.math_test_scores = math_test_scores
        self.total_points=total_points
        self.matrix_languauge = matrix_languauge
        self.matrix_math = matrix_math
        self.matrix_reading = matrix_reading
        self.admission_test_score_total = admission_test_score_total
        self.status = status
        self.matrix_languauge_retest = matrix_languauge_retest
        self.matrix_math_retest = matrix_math_retest
        self.matrix_reading_restest = matrix_reading_restest
        self.total_points_retest = total_points_retest
        self.updated_at = updated_at
        self.guardian1_email = guardian1_email
        self.guardian2_email = guardian2_email
        self.grade = grade
        self.deliver_test_accomodation_approved = deliver_test_accomodation_approved
        self.test_date_sign_up = test_date_sign_up
