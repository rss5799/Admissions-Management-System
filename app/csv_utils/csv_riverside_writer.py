import csv
from app.models import student
import pandas as pd
from app.services.matrix_calculator import lookup_matrix_points
from pathlib import Path
import json
import app


MATRIX_FILE = 'app/services/admissions_matrix.json'

with open(MATRIX_FILE, "r") as f:
    matrix = json.load(f)




def place_riverside_into_schoolmint():

    #pull the schoolmint file that's dropped into the system
    original_schoolmint_data_no_tests = ('SchoolMintNoTests.csv')
    with open(original_schoolmint_data_no_tests, 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Reads the first row, which is the header
        print(header)
    print(original_schoolmint_data_no_tests[0])
    #pull the riverside data that's dropped into the system
    original_riverside_data = ('DummyRiversideData.csv')

    #convert both to dataframes
    school_mint_df = pd.read_csv(original_schoolmint_data_no_tests)
    riverside_df = pd.read_csv(original_riverside_data)

    #join and drop nan values
    merged_results = pd.merge(school_mint_df, riverside_df, left_on='id', right_on='STUDENT ID 1')    
    merged_results = merged_results.fillna("")

    # #print statements to test    
    # print("ID:", merged_results.iloc[105]['id'])
    # print("matrix gpa initial:", merged_results.iloc[105]['matrix_gpa'])
    # print("math initial:", merged_results.iloc[105]['math_test_scores'], "matrix math initial:", merged_results.iloc[105]['matrix_math'])
    # print("language initial:", merged_results.iloc[105]['language_test_scores'], "matrix language initial:", merged_results.iloc[105]['matrix_languauge'])
    # print("reading initial:", merged_results.iloc[105]['reading_test_score'], "matrix reading initial:", merged_results.iloc[105]['matrix_reading'])
    # print("total points initial:", merged_results.iloc[105]['total_points'])

    # print("#################################################################")

    # print("math2 initial:", merged_results.iloc[105]['math_test_scores2'], "matrix math2 initial:", merged_results.iloc[105]['matrix_math_retest'])
    # print("language2 initial:", merged_results.iloc[105]['language_test_scores2'], "matrix language2 initial:", merged_results.iloc[105]['matrix_languauge_retest'])
    # print("reading2 initial:", merged_results.iloc[105]['reading_test_score2'], "matrix reading2 initial:", merged_results.iloc[105]['matrix_reading_restest'])
    # print("total points2 initial:", merged_results.iloc[105]['total_points_retest'])

    # print("#################################################################")
    

    #iterate down each row in the dataframe
    for index, row in merged_results.iterrows():
        #initial values
        matrix_gpa = 0
        reading_matrix = 0
        language_matrix = 0
        math_matrix = 0
        if(row['matrix_gpa']):
            matrix_gpa = row['matrix_gpa']

        #update values and move to columns (first columns if it's the first test...)
        if(row['reading_test_score'] == "" and row['language_test_scores'] == "" and row['math_test_scores'] == ""):
            if(row['READING TOTAL - NPR']):
                reading_matrix = lookup_matrix_points(row['READING TOTAL - NPR'], matrix["test_scores"])
                merged_results.loc[index, 'reading_test_score'] = row['READING TOTAL - NPR']
                merged_results.loc[index, 'matrix_reading'] = reading_matrix
            if(row['LANGUAGE TOTAL - NPR']):
                language_matrix = lookup_matrix_points(row['LANGUAGE TOTAL - NPR'], matrix["test_scores"])
                merged_results.loc[index, 'language_test_scores'] = row['LANGUAGE TOTAL - NPR']
                merged_results.loc[index, 'matrix_languauge'] = language_matrix
            if(row['MATH TOTAL - NPR']):
                math_matrix = lookup_matrix_points(row['MATH TOTAL - NPR'], matrix["test_scores"])
                merged_results.loc[index, 'math_test_scores'] = row['MATH TOTAL - NPR']
                merged_results.loc[index, 'matrix_math'] = math_matrix
            
            merged_results.loc[index, 'total_points'] = matrix_gpa + reading_matrix + language_matrix + math_matrix

        #update values and move to columns (second columns if it's the retest...)
        elif(row['reading_test_score2'] == "" and row['language_test_scores2'] == "" and row['math_test_scores2'] == ""):
            if(row['READING TOTAL - NPR']):
                reading_matrix = lookup_matrix_points(row['READING TOTAL - NPR'], matrix["test_scores"])
                merged_results.loc[index, 'reading_test_score2'] = row['READING TOTAL - NPR']
                merged_results.loc[index, 'matrix_reading_restest'] = reading_matrix
            if(row['LANGUAGE TOTAL - NPR']):
                language_matrix = lookup_matrix_points(row['LANGUAGE TOTAL - NPR'], matrix["test_scores"])
                merged_results.loc[index, 'language_test_scores2'] = row['LANGUAGE TOTAL - NPR']
                merged_results.loc[index, 'matrix_languauge_retest'] = language_matrix
            if(row['MATH TOTAL - NPR']):
                math_matrix = lookup_matrix_points(row['MATH TOTAL - NPR'], matrix["test_scores"])
                merged_results.loc[index, 'math_test_scores2'] = row['MATH TOTAL - NPR']
                merged_results.loc[index, 'matrix_math_retest'] = math_matrix

            
            merged_results.loc[index, 'total_points_retest'] = matrix_gpa + reading_matrix + language_matrix + math_matrix

    
    
    # print("ID:", merged_results.iloc[105]['id'])
    # print("matrix gpa final:", merged_results.iloc[105]['matrix_gpa'])
    # print("math final:", merged_results.iloc[105]['math_test_scores'], "matrix math final:", merged_results.iloc[105]['matrix_math'])
    # print("language final:", merged_results.iloc[105]['language_test_scores'], "matrix language final:", merged_results.iloc[105]['matrix_languauge'])
    # print("reading final:", merged_results.iloc[105]['reading_test_score'], "matrix reading final:", merged_results.iloc[105]['matrix_reading'])
    # print("total points final:", merged_results.iloc[105]['total_points'])

    # print("#################################################################")

    # print("math2 final:", merged_results.iloc[105]['math_test_scores2'], "matrix math2 final:", merged_results.iloc[105]['matrix_math_retest'])
    # print("language2 final:", merged_results.iloc[105]['language_test_scores2'], "matrix language2 final:", merged_results.iloc[105]['matrix_languauge_retest'])
    # print("reading2 final:", merged_results.iloc[105]['reading_test_score2'], "matrix reading2 final:", merged_results.iloc[105]['matrix_reading_restest'])
    # print("total points2 final:", merged_results.iloc[105]['total_points_retest'])

    # print("#################################################################")

    headers = ['id', 'matrix_gpa', 'language_test_scores', 'reading_test_score', 'math_test_scores', 'total_points', 'matrix_languauge', 'matrix_math', 'matrix_reading', 'status', 'matrix_languauge_retest', 'matrix_math_retest', 'matrix_reading_restest', 'total_points_retest', 'updated_at', 'guardian1_email', 'guardian2_email', 'grade', 'deliver_test_accomodation_approved', 'test_date_sign_up', 'current_school', 'gpa', 'language_test_scores2', 'reading_test_score2', 'math_test_scores2']
    merged_results.to_csv('riversideAddedToSchoolmint.csv', columns = headers)

place_riverside_into_schoolmint()