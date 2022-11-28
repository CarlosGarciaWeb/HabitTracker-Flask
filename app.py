from flask import Flask, render_template, request, url_for, redirect


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", title="Habit Tracker - Home")



@app.route("/add-habit", methods=["GET","POST"])
def add_habit():
    return render_template("add_habits.html", title="Add Habit")