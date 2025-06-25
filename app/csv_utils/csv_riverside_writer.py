import csv
from app.models import student

original_schoolmint_data = ('DummyDataComplete.csv')
original_riverside_data = ('DummyRiversideData.csv')

def update_schoolmint_with_riverside_scores():
     #fetch riverside data
     #for each id in riverside:
        #find the row in schoolmint
            #if language_test_scores,reading_test_score,math_test_scores are not empty:
                #if language_test_scores2,reading_test_score2,math_test_scores2 are not empty:
                    #return
                #else:
                    #get the matrix_score conversion
                    #popualate language_test_scores2,reading_test_score2,math_test_scores2, matrix_languauge_retest,matrix_math_retest,matrix_reading_restest,total_points_retest with riverside reading, language math
                    #write to schoolminte datafile
            #else:
                #get the matrix_score conversions
                #populate language_test_scores,reading_test_score,math_test_scores, matrix_languauge,matrix_math,matrix_reading, total_matrix with riverside reading,language, math
                #write to schoolmint datafile

def fetch_riverside_data(student_id):
        admissions_scores_dict = {}
        with open(original_riverside_data, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if str(row[header.index('STUDENT ID 1')]) == str(student_id):
                    admissions_scores_dict['id'] = student_id
                    admissions_scores_dict['reading'] = row[header.index('READING TOTAL - NPR')]
                    admissions_scores_dict['lanaguage'] = row[header.index('LANGUAGE TOTAL - NPR')]
                    admissions_scores_dict['math'] = row[header.index('MATH TOTAL - NPR')]
                    print(admissions_scores_dict)
                    return(admissions_scores_dict)
                

def write_riverside_scores_to_csv(student_id, language, language_matrix, reading, reading_matrix, math , math_matrix, total_points):
    rows = []
    with open(original_riverside_data, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
            if row['id'] == student_id:
                if row['language_test_scores'] == '':
                    row['language_test_scores'] = language
                    row['math_test_scores'] = math
                    row['reading_test_score'] = reading
                    row['matrix_languauge'] = language_matrix
                    row['matrix_reading'] = reading_matrix
                    row['matrix_math'] = math_matrix
                    row['total_points'] = total_points
                else:
                    row['language_test_scores2'] = language
 

    with open(original_schoolmint_data, 'w', newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = reader.fieldnames)    
        writer.writeheader()
        writer.writerows(rows)