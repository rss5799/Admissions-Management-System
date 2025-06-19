import csv
from app.models import student

original_schoolmint_data = ('DummyDataComplete.csv')
updated_schoolmint_data = ('updated_student_data.csv')

def fetch_updated_student_instance(student_id):
    with open(original_schoolmint_data, 'r') as file:
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
                return current_student
            

def write_gpa_to_csv(student_id, gpa, matrix_gpa):
    rows = []
    with open(original_schoolmint_data, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
            if row['id'] == student_id:
                row['gpa'] = gpa
                row['matrix_gpa'] = matrix_gpa
 

    with open(original_schoolmint_data, 'w', newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = reader.fieldnames)    
        writer.writeheader()
        writer.writerows(rows)
