import pytest
from app import create_app
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from app.models.DecisionTree import DecisionTreeRegressor
from app.models.train import update_csv_with_prediction_scores
from sklearn.metrics import mean_squared_error
import os
import csv
import random

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


def test_tree_instantiates():
    regressor = DecisionTreeRegressor()
    assert regressor is not None


def test_tree_mse_success_criteria():
    data = pd.read_csv('data/LongitudinalData.csv')
    data = data.fillna('')
    required_columns = ['Iowa Language', 'Iowa Math', 'Iowa Reading', 'Unweighted GPA']
    data = data[data[required_columns].ne('').all(axis=1)]
    data.rename(columns={'Iowa Language': 'ad_lang', 'Iowa Math': 'ad_math', 'Iowa Reading': 'ad_reading', 'Unweighted GPA': 'unweigh_gpa'}, inplace=True)

    feature_cols = ['ad_lang', 'ad_math', 'ad_reading']
    X = data.loc[:, feature_cols] .values
    Y = data['unweigh_gpa'].values.reshape(-1, 1)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = .2, random_state = 41)

    regressor = DecisionTreeRegressor(min_samples_split = 3, max_depth = 3)
    regressor.fit(X_train, Y_train)
    
    Y_pred = regressor.predict(X_test)
    assert np.sqrt(mean_squared_error(Y_test, Y_pred)) is not None
    assert np.sqrt(mean_squared_error(Y_test, Y_pred)) < 0.75

def test_tree_nodes_populate():
    data = pd.read_csv('data/LongitudinalData.csv')
    data = data.fillna('')
    required_columns = ['Iowa Language', 'Iowa Math', 'Iowa Reading', 'Unweighted GPA']
    data = data[data[required_columns].ne('').all(axis=1)]
    data.rename(columns={'Iowa Language': 'ad_lang', 'Iowa Math': 'ad_math', 'Iowa Reading': 'ad_reading', 'Unweighted GPA': 'unweigh_gpa'}, inplace=True)

    feature_cols = ['ad_lang', 'ad_math', 'ad_reading']
    X = data.loc[:, feature_cols] .values
    Y = data['unweigh_gpa'].values.reshape(-1, 1)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = .2, random_state = 41)

    regressor = DecisionTreeRegressor(min_samples_split = 3, max_depth = 3)
    regressor.fit(X_train, Y_train)
    
    Y_pred = regressor.predict(X_test)

    data = regressor.print_tree()
    assert data is not ''


def test_predicted_gpa_calculated():
    #make a copy of schoolmint for testing
    original_schoolmint = ('tests/SampleCsvsForTesting/schoolmintForPytest.csv')
    #make a copy of schoolmint for pytests
    if os.path.exists('tests/SampleCsvsForTesting/copyOfDataForTesting.csv'):
        os.remove('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    assert not os.path.exists('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    copy_for_testing = ('tests/SampleCsvsForTesting/copyOfDataForTesting.csv')
    with open(original_schoolmint, 'r', newline='') as infile:
        reader = csv.reader(infile)
        with open(copy_for_testing, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)
    #run copy through decision tree
    update_csv_with_prediction_scores(copy_for_testing)

    df = pd.read_csv(copy_for_testing).fillna('')
    print(df)

    for index, row in df.iterrows():
        if df.loc[index, 'status'] == "Eligible":
            assert df.loc[index, "Predicted Unweighted GPA"] != " "
        else:
            assert df.loc[index, "Predicted Unweighted GPA"] == " "


def test_pred_gpa_displayed_on_hlsv(client):
    response = client.get("/point_inputs/")
    assert b"Predicted Unweighted GPA" in response.data

def test_pred_gpa_displayed_on_student_profile(client):
    df = pd.read_csv('data/updated_schoolmint.csv').fillna('')
    random_ids = df['id'].sample(n=5)
    print(random_ids)
    for random_id in random_ids:
        if df.loc[df['id'] == random_id, 'status'].iloc[0] == "Eligible":
            route = '/student_details/?id_query='+ str(random_id)
            unweighted_gpa = df.loc[df['id'] == random_id, 'Predicted Unweighted GPA'].iloc[0]
            response = client.get(route)
            unweighted_gpa = str(unweighted_gpa).encode('utf-8')
            assert unweighted_gpa in response.data
