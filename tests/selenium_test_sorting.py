import pytest  
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from app import create_app




@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


#Unit Test 23
def test_sort_id_descending(client):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000/point_inputs/")
    sort_feature = driver.find_element(By.XPATH, '/html/body/form[2]/div/div[4]/div/div[2]/div/table/thead/tr/th[1]')
    sort_feature.send_keys(Keys.RETURN)
    response = client.get("/point_inputs/")
    assert response.status_code == 200

#Unit test 26
def test_sort_school_ascending(client):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000/point_inputs/")
    sort_feature = driver.find_element(By.XPATH, '/html/body/form[2]/div/div[4]/div/div[2]/div/table/thead/tr/th[6]')
    sort_feature.send_keys(Keys.RETURN)
    response = client.get("/point_inputs/")
    assert response.status_code == 200


#Unit test 27
def test_sort_school_descending(client):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000/point_inputs/")
    sort_feature = driver.find_element(By.XPATH, '/html/body/form[2]/div/div[4]/div/div[2]/div/table/thead/tr/th[6]')
    sort_feature.send_keys(Keys.RETURN)
    sort_feature.send_keys(Keys.RETURN)
    response = client.get("/point_inputs/")
    assert response.status_code == 200
