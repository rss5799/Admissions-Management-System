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
    original_schoolmint_data_no_tests = ('SchoolMintNoTests.csv')
    original_riverside_data = ('DummyRiversideData.csv')
    school_mint_df = pd.read_csv(original_schoolmint_data_no_tests)
    riverside_df = pd.read_csv(original_riverside_data)
    merged_results = pd.merge(school_mint_df, riverside_df, left_on='id', right_on='STUDENT ID 1')
    
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000) # Adjust width for better readability of wide DataFrames
    pd.set_option('display.max_colwidth', None) # Display full content of wide columns

    
    
    merged_results = merged_results.fillna("")
    
    print("ID:", merged_results.iloc[105]['id'])
    print("matrix gpa initial:", merged_results.iloc[105]['matrix_gpa'])
    print("math initial:", merged_results.iloc[105]['math_test_scores'], "matrix math initial:", merged_results.iloc[105]['matrix_math'])
    print("language initial:", merged_results.iloc[105]['language_test_scores'], "matrix language initial:", merged_results.iloc[105]['matrix_languauge'])
    print("reading initial:", merged_results.iloc[105]['reading_test_score'], "matrix reading initial:", merged_results.iloc[105]['matrix_reading'])
    print("total points initial:", merged_results.iloc[105]['total_points'])

    print("#################################################################")

    print("math2 initial:", merged_results.iloc[105]['math_test_scores2'], "matrix math2 initial:", merged_results.iloc[105]['matrix_math_retest'])
    print("language2 initial:", merged_results.iloc[105]['language_test_scores2'], "matrix language2 initial:", merged_results.iloc[105]['matrix_languauge_retest'])
    print("reading2 initial:", merged_results.iloc[105]['reading_test_score2'], "matrix reading2 initial:", merged_results.iloc[105]['matrix_reading_restest'])
    print("total points2 initial:", merged_results.iloc[105]['total_points_retest'])

    print("#################################################################")
    
    for index, row in merged_results.iterrows():
        if(row['reading_test_score'] == "" and row['language_test_scores'] == "" and row['math_test_scores'] == ""):
            matrix_gpa = 0
            reading_matrix = 0
            language_matrix = 0
            math_matrix = 0
            if(row['matrix_gpa']):
                matrix_gpa = row['matrix_gpa']
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

        elif(row['reading_test_score2'] == "" and row['language_test_scores2'] == "" and row['math_test_scores2'] == ""):
            matrix_gpa = 0
            matrix_gpa = 0
            reading_matrix = 0
            language_matrix = 0
            math_matrix = 0
            if(row['matrix_gpa']):
                matrix_gpa = row['matrix_gpa']
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

    
    
    print("ID:", merged_results.iloc[105]['id'])
    print("matrix gpa final:", merged_results.iloc[105]['matrix_gpa'])
    print("math final:", merged_results.iloc[105]['math_test_scores'], "matrix math final:", merged_results.iloc[105]['matrix_math'])
    print("language final:", merged_results.iloc[105]['language_test_scores'], "matrix language final:", merged_results.iloc[105]['matrix_languauge'])
    print("reading final:", merged_results.iloc[105]['reading_test_score'], "matrix reading final:", merged_results.iloc[105]['matrix_reading'])
    print("total points final:", merged_results.iloc[105]['total_points'])

    print("#################################################################")

    print("math2 final:", merged_results.iloc[105]['math_test_scores2'], "matrix math2 final:", merged_results.iloc[105]['matrix_math_retest'])
    print("language2 final:", merged_results.iloc[105]['language_test_scores2'], "matrix language2 final:", merged_results.iloc[105]['matrix_languauge_retest'])
    print("reading2 final:", merged_results.iloc[105]['reading_test_score2'], "matrix reading2 final:", merged_results.iloc[105]['matrix_reading_restest'])
    print("total points2 final:", merged_results.iloc[105]['total_points_retest'])

    print("#################################################################")

place_riverside_into_schoolmint()



# def update_schoolmint_with_riverside_scores():
#      #fetch riverside data
#     with open(original_riverside_data, 'r') as file:
#         reader = csv.reader(file)
#         header = next(reader)
#         for row in reader:
#             student_id = str(row[header.index('id')])
#             #find the row in schoolmint
#                 #if language_test_scores,reading_test_score,math_test_scores are not empty:
#                     #if language_test_scores2,reading_test_score2,math_test_scores2 are not empty:
#                         #return
#                     #else:
#                         #get the matrix_score conversion
#                         #popualate language_test_scores2,reading_test_score2,math_test_scores2, matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest with riverside reading, language math
#                         #write to schoolminte datafile
#                 #else:
#                     #get the matrix_score conversions
#                     #populate language_test_scores,reading_test_score,math_test_scores, matrix_languauge,matrix_math,matrix_reading, total_matrix with riverside reading,language, math
#                     #write to schoolmint datafile

# def fetch_riverside_data(student_id):
#         admissions_scores_dict = {}
#         with open(original_riverside_data, 'r') as file:
#             reader = csv.reader(file)
#             header = next(reader)
#             for row in reader:
#                 if str(row[header.index('STUDENT ID 1')]) == str(student_id):
#                     admissions_scores_dict['id'] = student_id
#                     admissions_scores_dict['reading'] = row[header.index('READING TOTAL - NPR')]
#                     admissions_scores_dict['lanaguage'] = row[header.index('LANGUAGE TOTAL - NPR')]
#                     admissions_scores_dict['math'] = row[header.index('MATH TOTAL - NPR')]
#                     print(admissions_scores_dict)
#                     return(admissions_scores_dict)
                

# def write_riverside_scores_to_csv(student_id, language, language_matrix, reading, reading_matrix, math , math_matrix, total_points):
#     rows = []
#     with open(original_riverside_data, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             rows.append(row)
#             if row['id'] == student_id:
#                 if row['language_test_scores'] == '':
#                     row['language_test_scores'] = language
#                     row['math_test_scores'] = math
#                     row['reading_test_score'] = reading
#                     row['matrix_languauge'] = language_matrix
#                     row['matrix_reading'] = reading_matrix
#                     row['matrix_math'] = math_matrix
#                     row['total_points'] = total_points
#                 else:
#                     row['language_test_scores2'] = language
#                     row['reading_test_score2'] = reading
#                     row['math_test_scores2'] = math
#                     row['matrix_languauge_retest'] = language_matrix
#                     row['matrix_math_retest'] = math_matrix
#                     row['matrix_reading_restest'] = reading_matrix
#                     row['total_points_retest'] = total_points
    
    
#     with open(original_schoolmint_data, 'w', newline = '') as file:
#         writer = csv.DictWriter(file, fieldnames = reader.fieldnames)    
#         writer.writeheader()
#         writer.writerows(rows)