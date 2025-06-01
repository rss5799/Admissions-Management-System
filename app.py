from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

count_testing = 10
count_processing = 20
count_eligible = 30
count_enrolled = 40
count_closed = 50

sample_data = {
    "item1": {"status": "Testing", "count": count_testing},
    "item2": {"status": "Processing", "count": count_processing},
    "item3": {"status": "Eligible", "count": count_eligible},
    "item4": {"status": "Enrolled", "count": count_enrolled},
    "item5": {"status": "Closed", "count": count_closed},
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exports/")
def exports():
    return render_template("exports.html")

@app.route("/status_overview/")
def status_overview():
    grouped_data = {}
    for item_id, item_data in sample_data.items():
        status = item_data["status"]
        if status not in grouped_data:
            grouped_data[status] = []
        grouped_data[status].append(item_data)
    return render_template("status_overview.html", grouped_data=grouped_data)


if __name__ == "__main__":
    app.run()