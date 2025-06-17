import csv
from app.models import student


def fetch_updated_student_instance(student_id):
    file_path = ('DummyDataComplete.csv')
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if str(row[header.index('id')]) == str(student_id):
                current_student = student.Student(
                    id = row[0],
                    gpa = row[21],
                    matrix_gpa = row[1],
                    language_test_scores = row[2],
                    reading_test_score = row[3],
                    math_test_scores =  row[4],
                    total_points = row[5],
                    matrix_languauge = row[6], 
                    matrix_math = row[7],
                    matrix_reading = row[8],
                    matrix_points_total= row[1] + row[6] + row[7] + row[8],
                    status = row[9],
                    matrix_languauge_retest = row[10],
                    matrix_math_retest = row[11],
                    matrix_reading_restest = row[12],
                    total_points_retest = row[13],
                    updated_at = row[14],
                    guardian1_email = row[15],
                    guardian2_email = row[16],
                    grade = row[17],
                    deliver_test_accomodation_approved = row[18],
                    test_date_sign_up = row[19],
                    current_school = row[20]
                )
                return(current_student)
