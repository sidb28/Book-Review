import os, requests

from flask import Flask, session, request, render_template, redirect, jsonify, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from authenticator import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "":
            return render_template("error.html", message = "No username provided")
        if password == "":
            return render_template("error.html", message = "No password provided")    

        usernames = db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).fetchone()

        if usernames:
            return render_template("error.html", message = "Duplicate username. Try another one!")

        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username":username, "password":password})
        db.commit()

        return redirect(url_for("login"))
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "":
            return render_template("error.html", message = "No username provided")
        if password == "":
            return render_template("error.html", message = "No password provided")

        matchedUser = db.execute("SELECT * FROM users WHERE username=:username AND password=:password", {"username":username, "password":password}).fetchone()

        if matchedUser is None:
            return render_template("error.html", message = "Username or Password is incorrect. Please try again!")

        session["user_id"] = matchedUser.id
        
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/search")
@login_required
def search():
    searched = request.args.get("book")
    if not searched:
        return render_template("error.html", message = "No search query provided!")
    
    searchLike = "%"+searched+"%"
    
    searchResults = db.execute("SELECT * FROM books WHERE title LIKE :searchLike OR author LIKE :searchLike OR isbn LIKE :searchLike", {"searchLike":searchLike}).fetchall()

    if not searchResults:
        return render_template("error.html", message = "No such books found!")

    return render_template("search.html", searchResults=searchResults)

@app.route("/review/<book_id>", methods=["GET", "POST"])
@login_required
def review(book_id):
    if request.method == "GET":

        book = db.execute("SELECT * FROM books WHERE id = :book_id", {"book_id":book_id}).fetchall()

        goodreads_res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GX1mV1Wp7BKvRsHiCw", "isbns": book[0][3]})

        api_data = goodreads_res.json()
        api_data = api_data['books'][0]
        book.append(api_data) # Store local data in book[0] as tuple, api data in book[1] as json
        
        reviews = db.execute("SELECT * FROM users JOIN reviews ON reviews.user_id = users.id WHERE book_id = :book_id", {"book_id":book_id}).fetchall()

        return render_template("book.html", book=book, reviews=reviews)

    elif request.method == "POST":

        rating = request.form.get("rating")
        description = request.form.get("description")
        user_id = session['user_id']

        checkDuplicate = db.execute("SELECT * from reviews WHERE user_id = :user_id AND book_id = :book_id", {"user_id":user_id, "book_id":book_id}).fetchone()

        if checkDuplicate is not None:
            return render_template("error.html", message = "You have already previously submitted a review for this book and cannot submit another.")
        else:
            db.execute( "INSERT INTO reviews (user_id, book_id, rating, description) VALUES (:user_id, :book_id, :rating, :description)", {"user_id":user_id, "book_id":book_id, "rating":rating, "description":description})
            db.commit()
            return render_template("success.html")

    else:
        return render_template("error.html", message = "Invalid Method Call!")

@app.route("/api/<isbn>")
@login_required
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
    if book is None:
        return "404 Error! No such book found"
    else:
        title = book['title']
        author = book['author']
        year = book['year']

        reviews = db.execute("SELECT COUNT(*), AVG(rating) FROM reviews WHERE book_id = :book_id", {"book_id":book['id']}).fetchall()

        review_count = reviews[0][0]
        average_score = reviews[0][1]
        if average_score is None:
            average_score = float()
        else:
            average_score = float(average_score)

        returnedBookInfo = {"title":title, "author":author, "year":year, "isbn":isbn, "review_count":review_count, "average_score":average_score}
        
        return jsonify(returnedBookInfo)