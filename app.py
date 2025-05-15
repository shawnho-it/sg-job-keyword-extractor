from flask import Flask, render_template, request
from scraper import run_scraper_and_return_data

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    logs = []
    job_data = []
    if request.method == "POST":
        job_role = request.form.get("job_role")
        min_salary = request.form.get("min_salary")
        logs, job_data = run_scraper_and_return_data(job_role, min_salary)

    return render_template("form.html", logs=logs, jobs=job_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

