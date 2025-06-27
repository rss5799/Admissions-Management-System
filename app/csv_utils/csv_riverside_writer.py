import csv
from app.models import student
import pandas as pd
from app.services.matrix_calculator import lookup_matrix_points
from pathlib import Path
import json
import app


#this function should be called when users press the button requesting that riverside data be merged with the most recent schoolmint csv
def place_riverside_into_schoolmint(schoolmintData, riversideResults):
    
    MATRIX_FILE = 'app/services/admissions_matrix.json'
    with open(MATRIX_FILE, "r") as f:
        matrix = json.load(f)

    #schoolMintData and riversideResults will be pulled from the file browser import page

    #convert both to dataframes
    school_mint_df = pd.read_csv(schoolmintData)
    riverside_df = pd.read_csv(riversideResults)

    school_mint_df['id'].astype(str)
    riverside_df['STUDENT ID 1'].astype(str)

    #join and drop nan values
    merged_results = pd.merge(school_mint_df, riverside_df, left_on='id', right_on='STUDENT ID 1', how = 'outer')    
    merged_results = merged_results.fillna("")

    #used to count the number of students whose records were updated (can be displayed to system user)
    counter = 0

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
            
            counter += 1
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

            counter += 1
            merged_results.loc[index, 'total_points_retest'] = matrix_gpa + reading_matrix + language_matrix + math_matrix

    headers = ['id', 'matrix_gpa', 'language_test_scores', 'reading_test_score', 'math_test_scores', 'total_points', 'matrix_languauge', 'matrix_math', 'matrix_reading', 'status', 'matrix_languauge_retest', 'matrix_math_retest', 'matrix_reading_restest', 'total_points_retest', 'updated_at', 'guardian1_email', 'guardian2_email', 'grade', 'deliver_test_accomodation_approved', 'test_date_sign_up', 'current_school', 'gpa', 'language_test_scores2', 'reading_test_score2', 'math_test_scores2']
    merged_results.to_csv(schoolmintData, columns = headers)

    return counter




