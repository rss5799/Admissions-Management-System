class Student:
    def __init__(self, id, gpa, matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, matrix_points_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up, current_school):
        self.id = id
        self.gpa = gpa
        self.matrix_gpa = matrix_gpa
        self.language_test_scores = language_test_scores
        self.reading_test_score = reading_test_score
        self.math_test_scores = math_test_scores
        self.total_points=total_points
        self.matrix_languauge = matrix_languauge
        self.matrix_math = matrix_math
        self.matrix_reading = matrix_reading
        self.matrix_points_total = matrix_points_total
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
        self.current_school = current_school
    