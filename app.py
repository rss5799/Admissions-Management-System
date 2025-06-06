import pandas as pd
import os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exports/")
def exports():
    return render_template("exports.html")

@app.route("/point_inputs/")
def point_inputs():
    return render_template("point_inputs.html")


@app.route("/upcoming_tests/")
def upcoming_tests():
    return render_template("upcoming_tests.html")

@app.route("/unresponsive_students/")
def unresponsive_students():
    return render_template("unresponsive_students.html")

if __name__ == "__main__":
    app.run()