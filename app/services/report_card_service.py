from pathlib import Path
import json
from app.services.matrix_calculator import calculate_gpa, lookup_matrix_points
from app.utils.csv_reader_writer import write_gpa_to_csv

class ReportCardService:
    def __init__(self, form, student):
        self.form = form
        self.student = student
        self.matrix = self._load_matrix()

    def _load_matrix(self):
        base_path = Path(__file__).resolve().parent
        matrix_path = Path(__file__).resolve().parent / "admissions_matrix.json"
        matrix_path = matrix_path.resolve()

        with matrix_path.open() as f:
            return json.load(f)

    def _safe_int(self, val):
        return int(val) if val not in ["", None] else 0

    def process(self):
        grades = {f: getattr(self.form, f).data.upper() for f in self.form._fields}
        gpa = calculate_gpa(grades)
        matrix_gpa = lookup_matrix_points(gpa, self.matrix["gpa"])

        total_points = sum([
            self._safe_int(self.student.matrix_language),
            self._safe_int(self.student.matrix_math),
            self._safe_int(self.student.matrix_reading),
            matrix_gpa
        ])

        total_points_retest = sum([
            self._safe_int(self.student.matrix_languauge_retest),
            self._safe_int(self.student.matrix_math_retest),
            self._safe_int(self.student.matrix_reading_restest),
            matrix_gpa
        ])

        write_gpa_to_csv(self.student.id, gpa, matrix_gpa, total_points, total_points_retest)

        return {
            "grades": grades,
            "gpa": gpa,
            "matrix_gpa": matrix_gpa,
            "total_points": total_points,
            "total_points_retest": total_points_retest
        }
