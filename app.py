import pandas as pd
import os
from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore, auth

app = Flask(__name__)

# Use your relative path to the credentials file (I don't know how to make this dynamic)
key_path = os.path.join(os.path.dirname(__file__), "/Users/taracan/Documents/SWENG894/Admissions-Management-System/app/credentials/firebase_key.json")
cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

class Student:
    def __init__(self, id,matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, admission_test_score_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest):
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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exports/")
def exports():
    return render_template("exports.html")

@app.route("/point_inputs/")
def point_inputs():
    return render_template("point_inputs.html")


@app.route("/upcoming_tests/")
def upcoming_tests():
    return render_template("upcoming_tests.html")

@app.route("/unresponsive_students/")
def unresponsive_students():
    return render_template("unresponsive_students.html")

@app.route("/student_details/", methods=['GET'])
def student_details():
    query = request.args.get('id_query')
    results = perform_student_search(query)
    if results:
        return render_template("student_details.html", results = results, query = query)
    else:
        return render_template("point_inputs.html", results = "Student Not Found", query = query)

def perform_student_search(query):
    # Access Firestore
    db = firestore.client()
    collection_ref = db.collection('student')
    docs = collection_ref.stream()
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
                current_student = Student(id, matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading,admission_test_score_total, status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest)
                return(current_student)
        



if __name__ == "__main__":
    app.run()