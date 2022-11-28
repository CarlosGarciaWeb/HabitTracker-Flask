from flask import Flask, render_template, request, url_for, redirect


# TODO: (End Goal) make a habit tracker for studying languages like Python, Go, Swift and link an api service that
# shows the weather for that particular date // add function that allows user to select periodicity of habit

app = Flask(__name__)

habits = ["Test Habits", "Second Habit Test"]

@app.route("/")
def home():
    return render_template("index.html", habits=habits,title="Habit Tracker - Home")



@app.route("/add-habit", methods=["GET","POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))
        redirect(url_for('home'))
    return render_template("add_habits.html", title="Add Habit")