# app/forms/report_card.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Regexp, Optional

grade_regex = r"^(?i:[A-D][+-]?|F)$"
grade_msg = "Enter A, B, C, D (with optional + or -), or F"

class ReportCardForm(FlaskForm):
    english        = StringField("English",        validators=[InputRequired(), Regexp(grade_regex, message=grade_msg)])
    math           = StringField("Math",           validators=[InputRequired(), Regexp(grade_regex, message=grade_msg)])
    science        = StringField("Science",        validators=[InputRequired(), Regexp(grade_regex, message=grade_msg)])
    social_studies = StringField("Social Studies", validators=[InputRequired(), Regexp(grade_regex, message=grade_msg)])
    language       = StringField("Language",       validators=[Optional(),      Regexp(grade_regex, message=grade_msg)])
