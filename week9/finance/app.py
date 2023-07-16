import os

import re
from urllib import response
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get user id from the session
    user_id = session.get("user_id")

    # Get symbol and total amount of share for each symbol
    rows = db.execute("SELECT symbol, SUM(shares) as total_shares FROM stocks WHERE user_id = ? GROUP BY (symbol)", user_id)

    total = 0
    # Find the current price of each symbol
    for row in rows:
        price = lookup(row["symbol"])
        row["price"] = price["price"]
        row["name"] = price["name"]
        row["total"] = row["price"] * row["total_shares"]
        total += row["total"]
        row["total"] = usd(row["total"])

    # Find the amount of cash the user have
    cash = db.execute("SELECT cash FROM users WHERE id = ? ", user_id)

    # Total cash
    total = total + cash[0]["cash"]

    return render_template("index.html", rows=rows, cash=usd(cash[0]["cash"]), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Validate user input
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("Missing symbol or shares!")

        # Check if the symbol is valid
        symbol = lookup(request.form.get("symbol"))

        if not symbol:
            return apology("Invalid Symbol!")

        # Check if user submitted a valid share

        if not request.form.get("shares").isdigit():
            return apology("Invalid Share!")

        elif not int(request.form.get("shares")) >= 1:
            return apology("Invalid Share!")

        share = int(request.form.get("shares"))

        total_share_price = symbol["price"] * share

        # User id
        id = session.get("user_id")

        # Cash the user have
        cash = db.execute("SELECT cash FROM users WHERE id= ?", id)

        # If user have enough cash to buy stocks
        if total_share_price > cash[0]["cash"]:
            return apology("Insufficient Cash : ( !")

        # Check in table called stocks and see if the user bought the stock before
        stock = db.execute("SELECT * FROM stocks WHERE id = ? AND symbol = ?", id, symbol["symbol"])

        # If the user already purchased a stock
        if len(stock) == 1:
            db.execute("UPDATE stocks SET shares = ? WHERE id = ? AND symbol = ?",
                       (stock[0]["shares"] + share), id, symbol["symbol"])

        # If the user didn't already purchase the stock
        elif len(stock) == 0:
            db.execute("INSERT INTO stocks(user_id, symbol, shares) VALUES (?, ?, ?)", id, symbol["symbol"], share)

        # Insert data into history
        history = db.execute("INSERT INTO history(user_id, symbol, shares, share_price, total) VALUES (?, ?, ?, ?, ?)",
                             id, symbol["symbol"], share, symbol["price"], total_share_price)

        if not history:
            return apology("ERROR!")

        # UPDATE the cash in the user table
        updated = db.execute("UPDATE users SET cash = ? WHERE id= ?", (cash[0]["cash"] - total_share_price), id)

        if not updated:
            return apology("Error! ")

        # Redirect to homepage

        return redirect("/", )

    else:
        # For Get request just render the html form!
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get all transctions of the user
    histories = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY (date) DESC", session["user_id"])
    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":

        # Check if user submitted the form.
        if not request.form.get("symbol"):
            return apology("Please input a Symbol!!")

        response = lookup(request.form.get("symbol"))

        # Check to see if the is a response from the function
        if not response:
            return apology("Invalid Symbol!")

        return render_template("quote.html", response=f"A share of {response['name']} ({response['symbol']})costs {usd(response['price'])}.")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Check
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Invalid Input! Please insert a username, password and confirmation!!")

        # Validate the username
        username = request.form.get("username")
        # Check if username only contain letters, numbers or underscore
        if not re.match("^[A-Za-z0-9_]*$", username):
            return apology("Username should contain only letters, numbers or underscores!")

            # Username should be between 3 and 12 characters
        elif not len(username) >= 3 or not len(username) <= 12:
            return apology("Username should be between 3 and 12 characters!")

        # Check if username exist
        temp_username = db.execute("SELECT username FROM users WHERE username = ?", username)
        if len(temp_username) == 1:
            return apology("Username already exist! Please login or choose a different username!")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password do not match!")

        id = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)",
                        username, generate_password_hash(request.form.get("password")))

        session["user_id"] = id

        return redirect("/")
    else:

        # If user is logged in redirect them to the index page
        if session.get("user_id"):
            return redirect("/")

        # Else just render the register page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Get user id from session
    user_id = session.get("user_id")

    if request.method == "POST":
        # Check if the user entered the data
        if not request.form.get("symbol") or not request.form.get("shares"):
            return apology("Missing symbol or share(s)!")

        # Validate the symbol by checking if it is valid
        symbol = lookup(request.form.get("symbol"))
        if not symbol:
            return apology("Invalid Symbol!")

        # Validate the share by checking if it is a digit and if it is greater or equal to 1
        if not request.form.get("shares").isdigit() and not int(request.form.get("shares")) >= 1:
            return apology("Invalid Share!")

        shares = int(request.form.get("shares"))

        # Check if the user bought a stock with the same symbol and check if the user have enough share to sell
        data = db.execute("SELECT * FROM stocks WHERE user_id = ? AND symbol= ?", user_id, symbol["symbol"])

        # If the lenght of data != 1 then it means the user did not buy a stock with that symbol
        if len(data) != 1:
            return apology("Invalid Symbol!")

        # Check if user have enough share to sell
        if shares > data[0]["shares"]:
            return apology("Insufficient Share(s)!")

        # Get the total price of all the shares to be sold
        total_price = shares * symbol["price"]

        # Update the stocks table

        final = (data[0]["shares"] - shares)

        # If the final share is 0 remove the stock from the table
        if final == 0:
            stocks = db.execute("DELETE FROM stocks WHERE user_id =? AND symbol = ?", user_id, symbol["symbol"])

        # Else update the table instead
        elif final > 0:
            stocks = db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?", final, user_id, symbol["symbol"])

        if not stocks:
            return apology("Error!", 403)

        # Update the cash in the users table

        users = db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_price, user_id)

        if not users:
            return apology("Error!", 403)

        # Add transaction to history
        history = db.execute("INSERT INTO history(user_id, symbol, shares, share_price, total) VALUES (?, ?, ?, ?, ?)",
                             user_id, symbol["symbol"], (-abs(shares)), symbol["price"], total_price)

        if not history:
            return apology("Error!", 403)

        return redirect("/")
    else:

        # Get all stock symbols the user bought
        symbols = db.execute("SELECT DISTINCT(symbol) FROM stocks WHERE user_id = ?", session.get("user_id"))
        return render_template("sell.html", symbols=symbols)


@app.route("/change", methods=["GET", "POST"])
def change():
    if request.method == "POST":

        # Check if user entered data into the form
        if not request.form.get("oldpassword") or not request.form.get("newpassword") or not request.form.get("confrimation"):
            return apology("Missing Fields!", 403)

        # Check if the old password is correct

        # Get password from table
        row = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Check password hash
        if not check_password_hash(row[0]["hash"], request.form.get("oldpassword")):
            return apology("Incorrect Password!", 403)

        # Check if the new password and confrimation are the same
        if request.form.get("newpassword") != request.form.get("confrimation"):
            return apology("New Password and Cofrimation password are not equal!", 403)

        # Update the new hash in the table
        password = db.execute("UPDATE users SET hash = ?  WHERE id = ? AND hash = ?",
                              generate_password_hash(request.form.get("newpassword")), session["user_id"], row[0]["hash"])

        return redirect("/")

    else:
        return render_template("change.html")