import csv

def filter_dict(data: dict) -> dict:
    """
    Filters out the 'csrf_token' key from a dictionary.
    
    Returns:
        A function that takes a dictionary and returns a new dictionary without the 'csrf_token' key.
    """
    filtered_data = {k: v for k, v in data.items() if k != 'csrf_token'}

    return filtered_data

def write_dummy_schoolmint_csv(path="data/updated_schoolmint.csv"):
    """
    Creates a dummy updated_schoolmint.csv file for testing purposes.

    This function writes a CSV file containing the expected headers and a single
    row of test data matching the structure required by the system. It ensures
    that automated tests relying on updated_schoolmint.csv can run without
    encountering missing columns or missing test data.

    Parameters
    ----------
    path : str, optional
        The file path where the CSV file should be created. Defaults to
        "data/updated_schoolmint.csv".

    """
    header = [
        "id", "gpa", "matrix_gpa", "language_test_scores", "reading_test_score",
        "math_test_scores", "total_points", "matrix_languauge", "matrix_math",
        "matrix_reading", "status", "matrix_languauge_retest", "matrix_math_retest",
        "matrix_reading_restest", "total_points_retest", "updated_at",
        "guardian1_email", "guardian2_email", "grade", "deliver_test_accomodation_approved",
        "test_date_sign_up", "current_school", "language_test_scores2",
        "reading_test_score2", "math_test_scores2"
    ]

    row = [
        "1", "3.5", "4", "90", "88", "92", "12", "4", "4", "4",
        "Active", "4", "4", "4", "12", "2024-07-02",
        "user1@email.com", "user2@email.com", "9", "Yes",
        "2024-08-15", "Other", "85", "88", "92"
    ]

    with open(path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(row)
