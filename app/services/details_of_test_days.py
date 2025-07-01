import pandas as pd
from app.models.testday import Testday
import math

def retrieve_unique_test_dates(schoolMintData:str):
    upcoming_test_dates = []

    df_schoolmint = pd.read_csv(schoolMintData)
    df_schoolmint = df_schoolmint.fillna("")

    for index, row in df_schoolmint.iterrows():
        test_value = row['test_date_sign_up']
        if(test_value != ""):
            if test_value not in upcoming_test_dates:
                upcoming_test_dates.append(test_value)
    return upcoming_test_dates


def retrieve_test_day_counts(schoolMintData:str, testday):
    df_schoolmint = pd.read_csv(schoolMintData)
    df_schoolmint = df_schoolmint.fillna("")
    test_day_deets = Testday(testday, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    for index, row in df_schoolmint.iterrows():
        if row['test_date_sign_up'] == testday:
            grade = str(row['grade'])
            accommsEligibility = str(row['deliver_test_accomodation_approved'])
            #if grade 8
            if grade == "9":
                #if first test
                if (row['language_test_scores'] == "" and row['reading_test_score'] == ""  and row['math_test_scores'] == ""):
                    #if standard time
                    if accommsEligibility != "Test Accommodations Approved":
                        test_day_deets.firststandard8 += 1                    
                    else:
                        test_day_deets.firstaccomms8 +=1
                else:
                    if accommsEligibility != "Test Accommodations Approved":
                        test_day_deets.reteststandard8 +=1
                    else:
                        test_day_deets.retestaccomms8 +=1
            elif grade == "10":
                #if first test
                if (row['language_test_scores'] == "" and row['reading_test_score'] == ""  and row['math_test_scores'] == ""):
                    #if standard time
                    if accommsEligibility != "Test Accommodations Approved":
                        test_day_deets.firststandard9 += 1                    
                    else:
                        test_day_deets.firstaccomms9 += 1                    
                else:
                    if accommsEligibility != "Test Accommodations Approved":
                        test_day_deets.reteststandard9 += 1                    
                    else:
                        test_day_deets.retestaccomms9 += 1                    
            else:
                #if first test
                if (row['language_test_scores'] == "" and row['reading_test_score'] == ""  and row['math_test_scores'] == ""):
                    #if standard time
                    if accommsEligibility != "Test Accommodations Approved":
                        test_day_deets.firststandard10 += 1 
                    else:
                        test_day_deets.firstaccomms10 += 1 
                else:
                    if accommsEligibility != "Test Accommodations Approved":
                        test_day_deets.reteststandard10 += 1 
                    else:
                        test_day_deets.retestaccomms10 += 1 
    test_day_deets.totalstandard = test_day_deets.firststandard8 + test_day_deets.firststandard9 + test_day_deets.firststandard10 + test_day_deets.reteststandard8 + test_day_deets.reteststandard9 + test_day_deets.reteststandard10
    test_day_deets.totalstandardrooms = math.ceil(test_day_deets.totalstandard / 25)
    test_day_deets.totalaccomms = test_day_deets.firstaccomms8 + test_day_deets.firstaccomms9 + test_day_deets.firstaccomms10 + test_day_deets.retestaccomms8 + test_day_deets.retestaccomms9 + test_day_deets.retestaccomms10
    test_day_deets.totalaccommsrooms = math.ceil(test_day_deets.totalaccomms / 25)
    test_day_deets.totalfirsttesters = test_day_deets.firststandard8 + test_day_deets.firststandard9 + test_day_deets.firststandard10 + test_day_deets.firstaccomms8 + test_day_deets.firstaccomms9 + test_day_deets.firstaccomms10
    test_day_deets.totalretesters = test_day_deets.reteststandard8 + test_day_deets.reteststandard9 + test_day_deets.reteststandard10 + test_day_deets.retestaccomms8 + test_day_deets.retestaccomms9 + test_day_deets.retestaccomms10
    test_day_deets.totalstudents = test_day_deets.totalfirsttesters + test_day_deets.totalretesters
    test_day_deets.totalrooms = test_day_deets.totalstandardrooms + test_day_deets.totalaccommsrooms

    return test_day_deets
