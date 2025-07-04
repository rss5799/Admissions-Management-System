import csv
from app.models import student


def fetch_updated_student_instance(student_id):
    original_schoolmint_data = ('data/updated_schoolmint.csv')
    with open(original_schoolmint_data, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if str(row[header.index('id')]) == str(student_id):
                current_student = student.Student(
                    id = row[header.index('id')],
                    gpa = row[header.index('gpa')],
                    matrix_gpa = row[header.index('matrix_gpa')],
                    language_test_scores = row[header.index('language_test_scores')],
                    reading_test_score = row[header.index('reading_test_score')],
                    math_test_scores =  row[header.index('math_test_scores')],
                    total_points = row[header.index('total_points')],
                    matrix_languauge = row[header.index('matrix_languauge')], 
                    matrix_math = row[header.index('matrix_math')],
                    matrix_reading = row[header.index('matrix_reading')],
                    status = row[header.index('status')],
                    matrix_languauge_retest = row[header.index('matrix_languauge_retest')],
                    matrix_math_retest = row[header.index('matrix_math_retest')],
                    matrix_reading_restest = row[header.index('matrix_reading_restest')],
                    total_points_retest = row[header.index('total_points_retest')],
                    updated_at = row[header.index('updated_at')],
                    guardian1_email = row[header.index('guardian1_email')],
                    guardian2_email = row[header.index('guardian2_email')],
                    grade = row[header.index('grade')],
                    deliver_test_accomodation_approved = row[header.index('deliver_test_accomodation_approved')],
                    test_date_sign_up = row[header.index('test_date_sign_up')],
                    current_school = row[header.index('current_school')],
                    language_test_scores2 = row[header.index('language_test_scores2')],
                    reading_test_score2 = 	row[header.index('reading_test_score2')],
                    math_test_scores2 = row[header.index('math_test_scores2')]
                )
                return current_student
    return(0)
            



def write_gpa_to_csv(student_id, gpa, matrix_gpa, total_points, total_points_retest):
    rows = []
    with open(original_schoolmint_data, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
            if row['id'] == student_id:
                row['gpa'] = gpa
                row['matrix_gpa'] = matrix_gpa
                row['total_points'] = total_points
                row['total_points_retest'] = total_points_retest
 

    with open(original_schoolmint_data, 'w', newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = reader.fieldnames)    
        writer.writeheader()
        writer.writerows(rows)
                

