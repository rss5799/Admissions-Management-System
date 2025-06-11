# class Student:
#     def __init__(self, id,matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading, admission_test_score_total,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest, updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up):
#         self.id = id
#         self.matrix_gpa = matrix_gpa
#         self.language_test_scores = language_test_scores
#         self.reading_test_score = reading_test_score
#         self.math_test_scores = math_test_scores
#         self.total_points=total_points
#         self.matrix_languauge = matrix_languauge
#         self.matrix_math = matrix_math
#         self.matrix_reading = matrix_reading
#         self.admission_test_score_total = admission_test_score_total
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

# students = []

# def load_students_from_firebase_into_array():
#     # Access Firestore
#     db = firestore.client()
#     collection_ref = db.collection('studentsXtraLite')
#     docs = collection_ref.stream()
#     for doc in docs:      
#         doc_data = doc.to_dict()
#         student = Student(
#             str(doc_data['id']),
#             str(doc_data['matrix_gpa']), 
#             str(doc_data['language_test_scores']),
#             str(doc_data['reading_test_score']),
#             str(doc_data['math_test_scores']),
#             str(doc_data['total_points']),
#             str(doc_data['matrix_languauge']),
#             str(doc_data['matrix_math']),
#             str(doc_data['matrix_reading']),
#             str(doc_data['matrix_languauge'] + doc_data['matrix_math'] + doc_data['matrix_reading']),
#             str(doc_data['status']),
#             str(doc_data['matrix_languauge_retest']),
#             str(doc_data['matrix_math_retest']),
#             str(doc_data['matrix_reading_restest']),
#             str(doc_data['total_points_retest']),
#             str(doc_data['updated_at']),
#             str(doc_data['guardian1_email']),
#             str(doc_data['guardian2_email']),
#             str(doc_data['grade']),
#             str(doc_data['deliver_test_accomodation_approved']),
#             str(doc_data['test_date_sign_up'])
#         )
#         students.append(student)
    