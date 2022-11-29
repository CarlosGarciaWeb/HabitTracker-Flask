from flask import Flask, render_template, request, url_for, redirect, Blueprint, current_app
import datetime
import uuid



# TODO: (End Goal) make a habit tracker for studying languages like Python, Go, Swift and link an api service that
# shows the weather for that particular date // add function that allows user to select periodicity of habit

pages = Blueprint("habits" ,__name__, template_folder="templates", static_folder="static")




@pages.context_processor
def add_calc_date_range():
    def selectDates(startDate: datetime.datetime):
        dates_list = [startDate + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates_list

    return {"date_range": selectDates}


def today_midnight():
    today = datetime.datetime.today()
    return datetime.datetime(today.year, today.month, today.day)


@pages.route("/")
def home():
    dates_string = request.args.get("date")
    if dates_string:
        selected_date = datetime.datetime.fromisoformat(dates_string)
    else:
        selected_date = today_midnight()

    habits_onDate = current_app.db.habitTracker.find({"added_date": {"$lte": selected_date}})

    completions = [habit["habit"] for habit in current_app.db.completions.find({"date": selected_date})]

    return render_template(
        "index.html",
        habits=habits_onDate,
        title="Habit Tracker - Home", 
        completions=completions,
        selected_date=selected_date
    )



@pages.route("/add-habit", methods=["GET","POST"])
def add_habit():
    today = today_midnight()
    if request.method == "POST":
        current_app.db.habitTracker.insert_one({"_id": uuid.uuid4().hex, "added_date": today, "name": request.form.get("habit")})
        return redirect(url_for('.home'))
    return render_template("add_habits.html", title="Add Habit", selected_date=today)




@pages.route("/completed", methods=["POST"])
def complete():
    date_string = request.form.get("date")
    habit = request.form.get("habitId")
    date = datetime.datetime.fromisoformat(date_string)

    current_app.db.completions.insert_one({"date": date, "habit": habit})

    return redirect(url_for('.home', date=date_string))