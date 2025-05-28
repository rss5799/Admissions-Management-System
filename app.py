from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exports/")
def exports():
    return render_template("exports.html")

@app.route("/status_overview/")
def status_overview():
    return render_template("status_overview.html")

#if __name__ == "__main__":
#    app.run()