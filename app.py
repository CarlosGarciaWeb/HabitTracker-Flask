from flask import Flask, render_template, request, url_for, redirect
import datetime
from collections import defaultdict

# TODO: (End Goal) make a habit tracker for studying languages like Python, Go, Swift and link an api service that
# shows the weather for that particular date // add function that allows user to select periodicity of habit

app = Flask(__name__)

habits = ["Test Habits", "Second Habit Test"]
completions = defaultdict(list)

@app.context_processor
def add_calc_date_range():
    def selectDates(startDate: datetime.date):
        dates_list = [startDate + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates_list

    return {"date_range": selectDates}


@app.route("/")
def home():
    dates_string = request.args.get("date")
    if dates_string:
        selected_date = datetime.date.fromisoformat(dates_string)
    else:
        selected_date = datetime.date.today()
    return render_template(
        "index.html",
        habits=habits,title="Habit Tracker - Home", 
        completions=completions[selected_date],
        selected_date=selected_date
    )



@app.route("/add-habit", methods=["GET","POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))
        return redirect(url_for('home'))
    return render_template("add_habits.html", title="Add Habit", selected_date=datetime.date.today())




@app.route("/completed", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)

    completions[date].append(habit)

    return redirect(url_for('home', date=date_string))