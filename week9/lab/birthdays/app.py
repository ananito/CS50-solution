from email import message
import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        # Validate the user input
        if not request.form.get("name") or not request.form.get("day") or not request.form.get("month"):
            return render_template("error.html", message="Invalid Input!")

        # Check if name is only letters
        name = request.form.get("name")

        if not name.isalpha():
            return render_template("error.html", message="Name should only contain letter!")

        # Check if the Day is not between 1 and 31
        day = int(request.form.get("day"))

        if not day >= 1 or not day <= 31:
            return render_template("error.html", message="Day of birth should be between 1 and 31!")

        month = int(request.form.get("month"))
        # Check if month is between 1 and 12
        if not month >= 1 or not month <= 12:
            return render_template("error.html", message="Birth Month should be between 1 and 12")

        # INSERT input into database
        db.execute("INSERT INTO birthdays(name, month, day) VALUES (?, ?, ?);", name, month, day)

        return redirect("/")

    else:

        # Get all birthdays from database
        birthdays = db.execute("SELECT * FROM birthdays;")

        return render_template("index.html", birthdays=birthdays)
