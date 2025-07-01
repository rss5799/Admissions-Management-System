import pytest
from app.services.details_of_test_days import retrieve_unique_test_dates, retrieve_test_day_counts
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

#Unit test 18
def test_retrieve_unique_test_dates():
    unique_tests = retrieve_unique_test_dates('tests/schoolmintForPytest.csv')
    assert len(unique_tests) == 2
    assert unique_tests[0] == 'January 18 2025'
    assert unique_tests[1] == 'March 5 2025'

#Unit test 19
def test_retrieve_test_day_counts():
    checking_test = retrieve_test_day_counts('tests/schoolmintForPytest.csv', 'January 18 2025')
    assert checking_test.date == 'January 18 2025'
    assert checking_test.firststandard8 == 0
    assert checking_test.firststandard9 == 1
    assert checking_test.firststandard10 == 0
    assert checking_test.firstaccomms8 == 1
    assert checking_test.firstaccomms9 == 0
    assert checking_test.firstaccomms10 == 0
    assert checking_test.reteststandard8 == 1
    assert checking_test.reteststandard9 == 2
    assert checking_test.reteststandard10 == 1
    assert checking_test.retestaccomms8 == 1
    assert checking_test.retestaccomms9 == 0
    assert checking_test.retestaccomms10 == 0
    assert checking_test.totalstandard == 5
    assert checking_test.totalstandardrooms == 1
    assert checking_test.totalaccomms == 2
    assert checking_test.totalaccommsrooms == 1
    assert checking_test.totalfirsttesters == 2
    assert checking_test.totalretesters == 5
    assert checking_test.totalstudents == 7
    assert checking_test.totalrooms == 2

    checking_test = retrieve_test_day_counts('tests/schoolmintForPytest.csv', 'March 5 2025')
    assert checking_test.date == 'March 5 2025'
    assert checking_test.firststandard8 == 0
    assert checking_test.firststandard9 == 0
    assert checking_test.firststandard10 == 0
    assert checking_test.firstaccomms8 == 0
    assert checking_test.firstaccomms9 == 0
    assert checking_test.firstaccomms10 == 0
    assert checking_test.reteststandard8 == 1
    assert checking_test.reteststandard9 == 0
    assert checking_test.reteststandard10 == 0
    assert checking_test.retestaccomms8 == 0
    assert checking_test.retestaccomms9 == 0
    assert checking_test.retestaccomms10 == 0
    assert checking_test.totalstandard == 1
    assert checking_test.totalstandardrooms == 1
    assert checking_test.totalaccomms == 0
    assert checking_test.totalaccommsrooms == 0
    assert checking_test.totalfirsttesters == 0
    assert checking_test.totalretesters == 1
    assert checking_test.totalstudents == 1
    assert checking_test.totalrooms == 1

#System test 23

def test_details_page_post(client):
    response = client.post("/upcoming_tests/")
    assert response.status_code == 200
    assert b"Choose a test date" in response.data
    response = client.get("/upcoming_tests/")
    assert response.status_code == 200
    assert b"Choose a test date" in response.data