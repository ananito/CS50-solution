from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    # Check if the user sumbitted any url
    if not request.args.get("q"):
        return redirect("/")
    url = "https://www.googleapis.com/books/v1/volumes?fields=items(volumeInfo/description,volumeInfo/title,volumeInfo/industryIdentifiers,volumeInfo/infoLink,volumeInfo/imageLinks/thumbnail,volumeInfo/publishedDate,volumeInfo/authors)&q="

    search = request.args.get("q")

    # Send the url request

    books = requests.get(url + search)

    # Change the result to JSON and enter into the ["item"] field
    books = books.json()["items"]
    return render_template("results.html", books=books, search=search)

    # return books
    # return render_template("results.html")


@app.route("/author/<name>")
def author(name=None):
    # Check if the user sumbitted any url
    if not name:
        return name
    url = "https://www.googleapis.com/books/v1/volumes?fields=items(volumeInfo/description,volumeInfo/title,volumeInfo/industryIdentifiers,volumeInfo/infoLink,volumeInfo/imageLinks/thumbnail,volumeInfo/publishedDate,volumeInfo/authors)&q=inauthor:"

    # send the url request
    books = requests.get(url + name)

    # Change the result to JSON and enter into the ["item"] field
    books = books.json()["items"]
    # return books
    return render_template("author.html", books=books, author=name)
