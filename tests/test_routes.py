import pytest
from app import create_app
import csv
from unittest.mock import patch
from app.models.student import Student
from app.utils.csv_reader_writer import fetch_updated_student_instance


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client





#System test 26:  Test enter report card route
def test_calculate_gpa_post(client):
    csv_file = "data/updated_schoolmint.csv"

    # Write dummy student row
    dummy_row = [
    "Joe",              # fname
    "Smith",            # lname
    "1",                # id
    "2005-01-01",       # dob
    "9",                # grade
    "0",                # gpa
    "0",                # matrix_gpa
    "0",                # language_test_scores
    "0",                # reading_test_score
    "0",                # math_test_scores
    "0",                # total_points
    "0",                # matrix_languauge
    "0",                # matrix_math
    "0",                # matrix_reading
    "",                 # status
    "0",                # matrix_languauge_retest
    "0",                # matrix_math_retest
    "0",                # matrix_reading_restest
    "0",                # total_points_retest
    "",                 # updated_at
    "",                 # guardian1_email
    "",                 # guardian2_email
    "0",                # deliver_test_accomodation_approved
    "",                 # test_date_sign_up
    "Other",            # current_school
    "0",                # language_test_scores2
    "0",                # reading_test_score2
    "0"                 # math_test_scores2
    #id,matrix_gpa,language_test_scores,reading_test_score,math_test_scores,total_points,matrix_languauge,matrix_math,matrix_reading,status,matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest,updated_at,guardian1_email,guardian2_email,grade,deliver_test_accomodation_approved,test_date_sign_up,current_school,gpa,language_test_scores2,reading_test_score2,math_test_scores2
]
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(dummy_row)

    # Set session to point to the student you just wrote
    with client.session_transaction() as sess:
        sess["current_id"] = "1"

    data = {
        'english': '90',
        'math': '85',
        'science': '95',
        'social_studies': '88',
        'language': '92'
    }
    response = client.post("/enter_report_card/", data=data)
    assert response.status_code == 200
    assert b"GPA" in response.data


#System test 27:  Test student details route (invalid query)
def test_student_search(client):
    response = client.get("/student_details/?id_query=12345")
    
    assert response.status_code == 302



#System test 28:  Test invalid route
def test_route_not_found(client):
    response = client.get("/this_route_does_not_exist")
    assert response.status_code == 404


#System test 29:  Test home route
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


#System test 30:  Test invalid route
def test_profile_route(client):
    response = client.get("/profile/12345")
    assert response.status_code == 404



#System test 32:  Test enter report card route
def test_enter_report_card_route(client):
    dummy_student = Student(
        id="1",
        gpa="0",
        matrix_gpa="0",
        language_test_scores="0",
        reading_test_score="0",
        math_test_scores="0",
        total_points="0",
        matrix_languauge="0",
        matrix_math="0",
        matrix_reading="0",
        status="",
        matrix_languauge_retest="0",
        matrix_math_retest="0",
        matrix_reading_restest="0",
        total_points_retest="0",
        updated_at="",
        guardian1_email="",
        guardian2_email="",
        grade="9",
        deliver_test_accomodation_approved="",
        test_date_sign_up="",
        current_school="Other",
        language_test_scores2="0",
        reading_test_score2="0",
        math_test_scores2="0",
        pred_gpa = "0"
    )

    with patch("app.routes.retrieve_current_student", return_value=dummy_student):
        with client.session_transaction() as sess:
            sess["current_id"] = "1"

        response = client.get("/enter_report_card/")
        assert response.status_code == 200

        # Provide dummy form data for the POST:
        data = {
            "english": "A",
            "math": "B",
            "science": "A",
            "social_studies": "B",
            "language": "A"
        }
        response = client.post("/enter_report_card/", data=data)
        response_data = response.get_data(as_text=True)
        assert "Return to Student Scores" in response_data

def test_user_signup_route(client):
        response = client.get("/signup")
        assert response.status_code == 200
        data = {
            "username" : "tmm259@psu.edu",
            "password" : "temp123"
        }
        response = client.post("/signup", data = data)
        response_data = response.get_data(as_text=True)
        assert "Account already exists" in response_data
        data = {
            "username" : "tmm@psu.edu",
            "password" : "temp123"
        }
        response_data = response.get_data(as_text=True)
        response = client.post("/signup", data = data)
        assert "Login" in response_data

        data = {
            "username" : "tmm@psu.edu",
            "password" : "temp123"
        }
        response_data = response.get_data(as_text=True)
        response = client.post("/signup", data = data)
        assert "Login" in response_data

def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_schoolmint_file_uploaded(client):
        data = {
            "schoolmintfile": "schoolmintfile"
        }
        response = client.post("/upload_csv", data = data)
        assert response.status_code == 200
