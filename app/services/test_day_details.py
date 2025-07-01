import pandas as pd

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



#load the current csv
#iterate down rows
#if not accoms get 8th, 9th, 10th
#if accoms get 8th, 9th, 10th
#return dictionary {test_date, standard8, standard9, standard10, accomms8, accomms9, accomms10, total, rooms}