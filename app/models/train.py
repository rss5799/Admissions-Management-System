from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from app.models.DecisionTree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

def update_csv_with_prediction_scores(student_data_csv):

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
    regressor.print_tree()

    Y_pred = regressor.predict(X_test)
    print(np.sqrt(mean_squared_error(Y_test, Y_pred)))


    #convert csv to dataframe
    data_frame_for_pred = pd.read_csv(student_data_csv).fillna('')

    data_frame_for_pred = data_frame_for_pred[data_frame_for_pred['status'] == 'Eligible']


    data_frame_for_pred["ad_lang"] = ""
    data_frame_for_pred["ad_math"] = ""
    data_frame_for_pred["ad_reading"] = ""

    data_frame_for_pred["Predicted Unweighted GPA"] = ''
    
    for index, row in data_frame_for_pred.iterrows():
        testOne = 0
        retest = 0
        if(data_frame_for_pred.loc[index, "language_test_scores"] != '' and data_frame_for_pred.loc[index, "math_test_scores"] != '' and data_frame_for_pred.loc[index, "reading_test_score"] != ''):
            testOne = data_frame_for_pred.loc[index, "language_test_scores"] + data_frame_for_pred.loc[index, "math_test_scores"] + data_frame_for_pred.loc[index, "reading_test_score"]
        if(data_frame_for_pred.loc[index, "language_test_scores2"] != '' and data_frame_for_pred.loc[index, "math_test_scores2"] != '' and data_frame_for_pred.loc[index, "reading_test_score2"] != ''):
            retest = data_frame_for_pred.loc[index, "language_test_scores2"] + data_frame_for_pred.loc[index, "math_test_scores2"] + data_frame_for_pred.loc[index, "reading_test_score2"]
        if(retest > 0):
            if(retest > testOne):
                data_frame_for_pred.loc[index, "ad_lang"] = data_frame_for_pred.loc[index, "language_test_scores2"]
                data_frame_for_pred.loc[index, "ad_math"] = data_frame_for_pred.loc[index, "math_test_scores2"]
                data_frame_for_pred.loc[index, "ad_reading"] = data_frame_for_pred.loc[index, "reading_test_score2"]
            else:
                data_frame_for_pred.loc[index, "ad_lang"] = data_frame_for_pred.loc[index, "language_test_scores"]
                data_frame_for_pred.loc[index, "ad_math"] = data_frame_for_pred.loc[index, "math_test_scores"]
                data_frame_for_pred.loc[index, "ad_reading"] = data_frame_for_pred.loc[index, "reading_test_score"]
        else:
            data_frame_for_pred.loc[index, "ad_lang"] = data_frame_for_pred.loc[index, "language_test_scores"]
            data_frame_for_pred.loc[index, "ad_math"] = data_frame_for_pred.loc[index, "math_test_scores"]
            data_frame_for_pred.loc[index, "ad_reading"] = data_frame_for_pred.loc[index, "reading_test_score"]

    required_columns = ['id', 'ad_lang', 'ad_math', 'ad_reading']
    data_frame_for_pred = data_frame_for_pred[data_frame_for_pred[required_columns].ne('').all(axis=1)]


    X = data_frame_for_pred.loc[:, feature_cols] .values
    Y = data_frame_for_pred['Predicted Unweighted GPA'].values.reshape(-1, 1)
    data_frame_for_pred['Predicted Unweighted GPA'] = regressor.predict(X)
    

    
    schoolmint_df = pd.read_csv(student_data_csv)
    schoolmint_df = pd.merge(schoolmint_df, data_frame_for_pred[['id', 'Predicted Unweighted GPA']], on='id', how='left')
    schoolmint_df = schoolmint_df.fillna('')
    for index, row in schoolmint_df.iterrows():
        for col_name, value in row.items():
            if(col_name != 'gpa' and col_name != 'Predicted Unweighted GPA' and isinstance(value, float)):
                value = int(value)
                schoolmint_df.loc[index, col_name] = value
            if(col_name == 'Predicted Unweighted GPA' and schoolmint_df.loc[index, "Predicted Unweighted GPA"] != ''):
                value = float(value)
                rounded_float = round(value, 4)
                schoolmint_df.loc[index, col_name] = rounded_float
    schoolmint_df.to_csv(student_data_csv, index=False)


############################################################
#code below works for decision tree and random forest classifiers

# data = datasets.load_breast_cancer()
# X = data.data
# y = data.target

# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size = 0.2, random_state=1234
# )


# clf = DecisionTree()
# clf.fit(X_train, y_train)
# predictions = clf.predict(X_test)

# def DTaccuracy(y_test, y_pred):
#     return np.sum(y_test == y_pred) / len(y_test)


# DTacc = DTaccuracy(y_test, predictions)

# print("Decision Tree Accuracy", DTacc)


# clf = RandomForest()
# clf.fit(X_train, y_train)
# predictions = clf.predict(X_test)


# def RFaccuracy(y_true, y_pred):
#     accuracy = np.sum(y_true == y_pred)/len(y_true)
#     return accuracy

# RFacc = RFaccuracy(y_test, predictions)
# print("Random Forest Accuracy", RFacc)