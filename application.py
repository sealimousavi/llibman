import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#quote api
res = requests.get("https://api.quotable.io/random")
data = res.json()
quote = data["content"] #bug to remove {
author = data["author"]
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///libman.db")

@app.route("/")
@login_required
def index():
    """Show books"""
    person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
    name = person[0]
    person = name['username']
    books = db.execute("SELECT title,author FROM books WHERE user = ? ORDER BY title", person)
    return render_template("index.html",books=books)


#welcome page to user
@app.route("/welcome")
def welcome():

    res = requests.get("https://api.quotable.io/random")
    data = res.json()
    quote = data["content"] 
    author = data["author"]
    return render_template("welcome.html",quote=quote,author=author)


#about page
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """add book to your library"""
    # check request is post
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return apology("insert a title not empty value")
        author = request.form.get("author")
        if not author:
            return apology("please insert author of this book")
        person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        name = person[0]
        person = name['username']

        db.execute("INSERT INTO books (title, author, user) VALUES(?,?, ?)",
                    title, author, person)
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html",)

@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """remove book from your library"""
    # check request is post
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return apology("insert a title not empty value")
       
        person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        name = person[0]
        person = name['username']

        db.execute("DELETE FROM books WHERE title LIKE ? AND user LIKE ?",
                    title, person)
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("remove.html",)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    return render_template("search.html")

@app.route("/searched", methods=["GET", "POST"])
@login_required
def searched():
    person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
    name = person[0]
    person = name['username']
    
    q = request.args.get("q")
    if q:
        books = db.execute("SELECT * FROM books WHERE title LIKE ? AND user LIKE ? OR author LIKE ? AND user LIKE ?","%" + request.args.get("q") + "%", person,"%" + request.args.get("q") + "%", person )
    else:
        books = []
    return jsonify(books)


@app.route("/lend", methods=["GET", "POST"])
@login_required
def lend():
    """lend book from your library"""
    # check request is post
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            return apology("insert a title not empty value")
        check_title = db.execute("SELECT title FROM books WHERE title =?", title)
        if not check_title:
            return apology("you don't have this book")
        friend = request.form.get("friend")
        if not friend:
            return apology("please insert author of this book")
        person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        name = person[0]
        person = name['username']
        author = db.execute("SELECT author FROM books WHERE title=?", title)
        author = author[0]['author']
        #check if user has that book

        db.execute("INSERT INTO lends (user, title, author, friend) VALUES(?, ?,?, ?)",
                    person ,title, author, friend)
        db.execute("DELETE FROM books WHERE title LIKE ? AND user LIKE ?",
                    title, person)
        books = db.execute("SELECT title,author,friend FROM lends WHERE user = ?", person)
        return redirect("/lended")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("lend.html",)

@app.route("/lended", methods=["GET", "POST"])
@login_required
def lended():
    if request.method == "POST":
        person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        name = person[0]
        person = name['username']
        books = db.execute("SELECT title,author,friend FROM lends WHERE user = ?", person)
        if request.method == "POST":
            title = request.form.get("title")
            author = db.execute("SELECT author FROM lends WHERE title=?", title)
            author = author[0]['author']
            db.execute("DELETE FROM lends WHERE title=? AND user=?", title, person)
            db.execute("INSERT INTO books (user, title, author) VALUES(?, ?, ?)", person, title, author)
        return redirect("/lended")
    else:
        person = db.execute("SELECT username FROM users WHERE id=?", session["user_id"])
        name = person[0]
        person = name['username']
        books = db.execute("SELECT title,author,friend FROM lends WHERE user = ?", person)
        return render_template("lended.html",books=books)

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



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Get username and password from form
        username = request.form.get("username")

        password = request.form.get("password")
        password2 = request.form.get("confirmation")
        if password != password2:
            return apology("Passwords doesn't match")

        # Ensure username and password were submitted
        if not username or not password:
            return apology("missing username or password")

        # Ensure username doesn't exist
        result = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if result:
            return apology("Username already taken!")
        # Register user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        # Remember user in session
        session["username"] = username

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
