import pytest
import csv
import pandas
from app.utils.csv_riverside_writer import combine_data


#Unit test 17: Ensure that all IDs are preserved when transfering Riverside test scores into SchoolMint
def test_ids_align():
     #open original schoolmint for pytests
    original_schoolmint = str('tests/SampleCsvsForTesting/schoolmintForPytest.csv')
    ids_in_OG_schoolmint = []
    ids_in_OG_riverside = []
    ids_in_combined = []

    with open(original_schoolmint, 'r', newline ='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids_in_OG_schoolmint.append(float(row['id']))

    #make a copy of schoolmint for pytests    
    copy_for_testing = str('tests/SampleCsvsForTesting/copyOfDataForIDTesting.csv')
    
    with open(original_schoolmint, 'r', newline='') as infile:
        reader = csv.reader(infile)
        with open(copy_for_testing, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                writer.writerow(row)
    
    #open riverside for pytests
    riverside_dummy_for_pytest = ('tests/SampleCsvsForTesting/riversideForPytest.csv')
    with open(riverside_dummy_for_pytest, 'r', newline ='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            ids_in_OG_riverside.append(float(row['STUDENT ID 1']))

    combine_data(copy_for_testing, riverside_dummy_for_pytest)

    with open(copy_for_testing, 'r', newline ='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] != "":
                ids_in_combined.append(float(row['id']))

    for id in ids_in_OG_schoolmint:
        #assert all ids from schoolmint made it to the combined file
        assert id in ids_in_combined

    for id in ids_in_OG_riverside:
        #assert all ids from riverside that existed in schoolmint made it to the combined file
        if id in ids_in_OG_schoolmint:
            assert id in ids_in_combined

        


