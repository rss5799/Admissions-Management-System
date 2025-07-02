import json
from pathlib import Path
from app.utils.helpers import filter_dict

current_dir = Path(__file__).parent
MATRIX_FILE = current_dir / "admissions_matrix.json"

with open(MATRIX_FILE, "r") as f:
    matrix = json.load(f)

# Convert letter grades to points
GRADE_TO_POINTS = {
    "A": 4,
    "B": 3,
    "C": 2,
    "D": 1,
    "F": 0
}

def calculate_gpa(grades):
    filtered_grades = filter_dict(grades)
    total_points = 0
    num_classes = 0

    for subject, letter_grade in filtered_grades.items():
        points = GRADE_TO_POINTS.get(letter_grade.upper(), 0)
        total_points += points
        num_classes += 1

    if num_classes == 0:
        return 0

    return round(total_points / num_classes, 2)

def lookup_matrix_points(value, table):
    for row in table:
        if row["min"] <= value <= row["max"]:
            return row["points"]
    return 0

def calculate_total_matrix(grades, reading, language, math):
    gpa = calculate_gpa(grades)
    gpa_points = lookup_matrix_points(gpa, matrix["gpa"])
    reading_points = lookup_matrix_points(reading, matrix["test_scores"])
    language_points = lookup_matrix_points(language, matrix["test_scores"])
    math_points = lookup_matrix_points(math, matrix["test_scores"])

    total = gpa_points + reading_points + language_points + math_points

    return {
        "gpa": gpa,
        "gpa_points": gpa_points,
        "reading_points": reading_points,
        "language_points": language_points,
        "math_points": math_points,
        "total_matrix_score": total
    }

#####################################################################################
# This is an example case. Uncomment it, update values, and run directly to test.   #
#####################################################################################
# if __name__ == "__main__":
#     sample_grades = {
#         "english": "A",
#         "math": "B",
#         "science": "A",
#         "social_studies": "B",
#         "language": "C"
#     }

#     result = calculate_total_matrix(sample_grades, reading=88, language=98, math=98)

#     print(json.dumps(result, indent=4))

