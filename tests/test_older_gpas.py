import pytest
from app import create_app
from app.services.matrix_calculator import matrix, calculate_gpa, calculate_total_matrix
from app.services.report_card_service import ReportCardService

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_older_semester(client):
        response = client.get("/enter_report_card/")
        assert response.status_code == 200
        response_data = response.get_data(as_text=True)
        assert "10th grade semester/trimester" in response_data
        assert "10th grade quarters" in response_data
        assert "11th grade semester/trimester" in response_data
        assert "11th grade quarters" in response_data


def test_11th_calculate_gpa_semesters():
    grades = {
        "english9S1": "",
        "math9S1": "",
        "science9S1": "",
        "social_studies9S1": "",
        "language9S1": "",
        "english9S2": "",
        "math9S2": "",
        "science9S2": "",
        "social_studies9S2": "",
        "language9S2": "",
        "english10S1": "",
        "math10S1": "",
        "science10S1": "",
        "social_studies10S1": "",
        "language10S1": ""
    }

    list_of_grades = []
    list_of_grades.append(['A','A','A','A','A','A','A','A','A','A','A','A','A','A','A', 4.0])
    list_of_grades.append(['A', 'B','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B', 'A', 3.53])
    #for course in grades:
    for item in list_of_grades:
        grades['english9S1'] = item[0]
        grades['math9S1'] = item[1]
        grades['science9S1'] = item[2]
        grades['social_studies9S1'] = item[3]
        grades['language9S1'] = item[4]
        grades['english9S2'] = item[5]
        grades['math9S2'] = item[6]
        grades['science9S2'] = item[7]
        grades['social_studies9S2'] = item[8]
        grades['language9S2'] = item[9]
        grades['english10S1'] = item[10]
        grades['math10S1'] = item[11]
        grades['science10S1'] = item[12]
        grades['social_studies10S1'] = item[13]
        grades['language10S1'] = item[14]
        gpa = item[15]
        assert gpa == calculate_gpa(grades)


def test_11th_calculate_gpa_quarters():
    grades = {
        "english9Q1": "",
        "math9Q1": "",
        "science9Q1": "",
        "social_studies9Q1": "",
        "language9Q1": "",
        "english9Q2": "",
        "math9Q2": "",
        "science9Q2": "",
        "social_studies9Q2": "",
        "language9Q2": "",
        "english9Q3": "",
        "math9Q3": "",
        "science9Q3": "",
        "social_studies9Q3": "",
        "language9Q3": "",
        "english9Q4": "",
        "math9Q4": "",
        "science9Q4": "",
        "social_studies9Q4": "",
        "language9Q4": "",
        "english10Q1": "",
        "math10Q1": "",
        "science10Q1": "",
        "social_studies10Q1": "",
        "language10Q1": "",
        "english10Q2": "",
        "math10Q2": "",
        "science10Q2": "",
        "social_studies10Q2": "",
        "language10Q2": ""
    }

    list_of_grades = []
    list_of_grades.append(['A','A','A','A','A','A','A','A','A','A','A','A','A','A','A', 'A','A','A','A','A','A','A','A','A','A','A','A','A','A','A',4.0])
    list_of_grades.append(['A', 'B','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B', 'A','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B','A', 'B', 'A', 3.5])
    #for course in grades:
    for item in list_of_grades:
        grades['english9Q1'] = item[0]
        grades['math9Q1'] = item[1]
        grades['science9Q1'] = item[2]
        grades['social_studies9Q1'] = item[3]
        grades['language9Q1'] = item[4]
        grades['english9Q2'] = item[5]
        grades['math9Q2'] = item[6]
        grades['science9Q2'] = item[7]
        grades['social_studies9Q2'] = item[8]
        grades['language9Q2'] = item[9]
        grades['english9Q3'] = item[10]
        grades['math9Q3'] = item[11]
        grades['science9Q3'] = item[12]
        grades['social_studies9Q3'] = item[13]
        grades['language9Q3'] = item[14]
        grades['english9Q4'] = item[15]
        grades['math9Q4'] = item[16]
        grades['science9Q4'] = item[17]
        grades['social_studies9Q4'] = item[18]
        grades['language9Q4'] = item[19]
        grades['english10Q1'] = item[20]
        grades['math10Q1'] = item[21]
        grades['science10Q1'] = item[22]
        grades['social_studies10Q1'] = item[23]
        grades['language10Q1'] = item[24]
        grades['english10Q2'] = item[25]
        grades['math10Q2'] = item[26]
        grades['science10Q2'] = item[27]
        grades['social_studies10Q2'] = item[28]
        grades['language10Q2'] = item[20]
        gpa = item[30]
        assert gpa == calculate_gpa(grades)