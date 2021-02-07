import os, requests

from flask import Flask, session, render_template, request, redirect, url_for,flash, jsonify, Markup
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta, date, datetime


app = Flask(__name__)
Session(app)
app.permanent_session_lifetime = timedelta(minutes=60)

user = 0
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
def index1():
    return render_template('book/index.html')

@app.route("/login")
def index():
    return render_template('book/index.html')

@app.route("/registrationPage", methods=["POST", "GET"])
def registrationPage():
    return render_template('book/registrationPage.html')

@app.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method == "GET":
        return render_template('book/registrationPage.html')
    name = request.form.get("name")
    surname = request.form.get("surname")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    select = "SELECT id FROM users WHERE username = :username"
    insert = "INSERT INTO users (name, surname, username, password) VALUES (:name, :surname, :username, :password)"
    
    if password != confirm:
        flash("Password does not match")
        return  redirect(url_for('registrationPage'))
    
    user_id = db.execute(select,{"username": username}).rowcount
 
    if user_id != 0:
        flash("username is not available, please choose another one!")
        return redirect(url_for('registrationPage'))
        
    db.execute(insert,{"name":name, "surname": surname, "username": username, "password": password})
    db.commit()

    flash("You are successful registered in Books review store website!")
    return  redirect(url_for('index'))

@app.route("/search", methods=["POST"])
def login():
    
    username = request.form.get("username")
    password = request.form.get("password")
    select = "SELECT * FROM users WHERE username = :username AND password = :password"

    if username == "" and password == "":
        flash("Username and Password are required field*")
        return redirect(url_for('index'))
    if username == "":
        flash("Username is a required field*")
        return redirect(url_for('index'))
    if password == "":
        flash("Password is a required field*")
        return redirect(url_for('index'))
   
    if db.execute(select,{"username": username, "password": password}).rowcount == 0:
        flash("Sign-on failed. Username or Password is incorrect**")
        return redirect(url_for('index'))

    select = "SELECT * FROM users WHERE username = :username"
    user_id = db.execute(select,{"username": username}).fetchone()

    session.permanent = True
    session["user_id"] = user_id[0]
    user = user_id[0]
    select = "SELECT name, surname FROM users WHERE id = :id"
    name = db.execute(select, {"id": user}).fetchone()
    select = "SELECT title, isbn, year, author FROM books ORDER BY RANDOM() LIMIT 25"
    books = db.execute(select).fetchall()
    return render_template('book/search.html',name=name, books=books)

@app.route("/search", methods=["GET"])
def check():
    if session.get("user_id") is not None:
        select = "SELECT title, isbn, year, author FROM books ORDER BY RANDOM() LIMIT 40"
        books = db.execute(select).fetchall()
        name = db.execute(select, {"id": user}).fetchone()
        return render_template('book/search.html',name=name,books=books)

    return redirect(url_for('index'))

@app.route("/loginout")
def logout():
    session.clear()
    flash("You are signed out!")
    return redirect(url_for('index'))

@app.route("/book", methods=["POST","GET"])
def book():
    if session.get("user_id") is None:
        return redirect(url_for('index'))

    select = "SELECT name, surname FROM users WHERE id = :id"
    user = session["user_id"]
    name = db.execute(select, {"id": user}).fetchone()
    select = "SELECT * FROM books WHERE isbn ILIKE :isbn OR title ILIKE :title OR author ILIKE :author"
    
    if request.method == "POST":
        book = request.form.get("book")
        getbook = db.execute(select,{"isbn":"%"+book+"%", "title": "%"+book+"%", "author":"%"+book+"%"}).fetchall()
        session["getbook"] = getbook  
        if not getbook:
            return render_template('book/noBookFound.html',name=name) 
    if request.method == "GET":
        if not session.get("getbook"):
            return render_template('book/noBookFound.html',name=name)

    return render_template('book/results.html', books=session.get("getbook"),name=name)

@app.route("/details/<string:isbn>", methods=["POST","GET"])
def details(isbn):
    if session.get("user_id") is None:
        return redirect(url_for('index'))

    if request.method == "GET":
        session['isbn'] = isbn
    session["isbn"] = isbn
    user_id = session["user_id"]
    isbn_id = db.execute("SELECT id FROM books WHERE isbn = :isbn",{"isbn": isbn}).fetchone()
    isbn_id = isbn_id[0]
    book = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn",{"isbn": isbn}).fetchone()
    
    select = "SELECT name, surname, reviews, time, rate, realtime FROM reviews JOIN users ON users.id = reviews.user_id JOIN books ON books.id = reviews.isbn_id WHERE isbn_id = :isbn_id AND LENGTH(reviews) > 0"
    reviews = db.execute(select, {"isbn_id":isbn_id}).fetchall()
    select = "SELECT title, isbn, author, year FROM reviews JOIN users ON users.id = reviews.user_id JOIN books ON books.id = reviews.isbn_id WHERE user_id = :user_id"

    favorite = db.execute(select, {"user_id":user_id}).fetchall()
    select = "WITH c AS (SELECT isbn_id ,rate, count(*) as cnt FROM reviews WHERE rate > 0 and isbn_id = :isbn_id GROUP BY isbn_id, rate ORDER BY rate desc) select 100.0* cnt/(SELECT SUM(cnt) FROM c ) as percentage FROM c"
    percentage = db.execute(select,{"isbn_id":isbn_id}).fetchall()
    select = "WITH a AS (WITH c AS (SELECT rate FROM reviews WHERE isbn_id = :isbn_id) SELECT count(*) FROM c GROUP BY rate) SELECT count(*) FROM a"
    numberrated = db.execute(select, {"isbn_id": isbn_id}).fetchone()
    select = "SELECT rate, sum(rate) FROM reviews WHERE isbn_id = :isbn_id GROUP BY rate HAVING count(*) > 0 ORDER BY rate DESC"
    numberorder = db.execute(select, {"isbn_id": isbn_id}).fetchall()
    leftside = '<div class="level" style = "border: 3px solid #cc5b10; width:'
    rightside ='%; border-radius: 4px"></div>'

 
   
    i = 0
    ratelist = [None] * 5
    avg = 0
    j= 0
    while i < numberrated[0]:
        if not percentage:
            pass
        else:
            fulldiv = leftside + str(percentage[i][0] - 3)+ rightside
            avg+= numberorder[i][1]
            j += numberorder[i][1]/numberorder[i][0]
            rate = Markup(fulldiv)
            div = Markup(fulldiv)
            ratelist[numberorder[i][0] - 1] = div
        i +=1
    if j > 0:
        avg = avg/j
    total_voted = int(j)

    j = 0
    for i in ratelist:
        if i is None:
            ratelist[j] = Markup('<div></div>')
        
        j +=1
    
    ratelist = ratelist[:: -1]
    reviews = reviews[:: -1]
    select = "SELECT name, surname FROM users WHERE id = :id"
    user = session["user_id"]

    name = db.execute(select, {"id": user}).fetchone()
    return render_template('book/review.html', book=book, reviews=reviews, name=name,rate=ratelist,avg=avg,total_voted=total_voted,favorite=favorite)


@app.route("/review", methods=["POST"])
def review():
    if session.get("user_id") is None:
        return redirect(url_for('index'))
   
    if request.method == "POST":
        if request.form.get("cancel"):
            return redirect(('details/' + session["isbn"]))
        
        user_id = session["user_id"]
        isbn = session["isbn"]
        rate = 0
        for i in range(0,6):
            if request.form.get("star"+str(i)+"") is not None:
                rate = i
            i = + 1
        review = request.form.get("reviews")
        today = date.today()
        now = datetime.now()
        now = str(now.hour) +":" + str(now.minute)
        time = today.strftime("%b %d ,%Y")

        if review is None or review == "":
            if rate == 0:
                
                flash(" Write any comment or rate the book instead")
                return redirect(('details/' + isbn))
        
        # check if the book has reviewed already
        isbn_id = db.execute("SELECT id FROM books WHERE isbn = :isbn",{"isbn": isbn}).fetchone()
        isbn_id = isbn_id[0]
        select_user = "SELECT * FROM reviews JOIN users ON users.id = reviews.user_id JOIN books ON books.id = reviews.isbn_id WHERE user_id = :user_id AND isbn_id = :isbn_id"
        
        reviewed = db.execute(select_user,{"user_id":user_id, "isbn_id": isbn_id}).fetchone()
        if reviewed is None:
            db.execute("INSERT INTO reviews (user_id, isbn_id, reviews, time, rate, realtime) VALUES (:user_id, :isbn_id, :reviews, :time, :rate, :realtime)",
                       {"user_id": user_id, "isbn_id": isbn_id, "reviews":review, "time": time, "rate":rate, "realtime": now})
            db.commit()
            return redirect(('details/' + isbn))        
        else:
            timereviewed = reviewed.time
            now = reviewed.realtime
            flash("You reviewed this book in " + timereviewed + " at "+ now)
            return redirect(('details/' + isbn))

@app.route("/popular")
def popular():
    if session.get("user_id") is None:
        return redirect(url_for('index'))
   
    user = session["user_id"]
    select = "SELECT name, surname FROM users WHERE id = :id"
    name = db.execute(select, {"id": user}).fetchone()
    select = "SELECT title, isbn, author, year FROM reviews JOIN users ON users.id = reviews.user_id JOIN books ON books.id = reviews.isbn_id WHERE user_id = :user_id"

    books = db.execute(select,{"user_id": user}).fetchall()
    select = "SELECT title, isbn, author, year FROM reviews JOIN users ON users.id = reviews.user_id JOIN books ON books.id = reviews.isbn_id WHERE user_id = :user_id"

    return render_template('book/search.html',name=name, books=books)

@app.route("/api/book_review/<string:isbn>", methods=["GET"])
def api(isbn):
    if session.get("user_id") is None:
            return redirect(url_for('index'))

    if request.method != "GET":
        flash("Read the API documantion")
        return  redirect(url_for('index'))
    session["isbn"] = isbn
    user_id = session["user_id"]
    isbn_id = db.execute("SELECT id FROM books WHERE isbn = :isbn",{"isbn": isbn}).fetchone()
    
    if isbn_id is None:
        return jsonify({"error": "No book with an isbn " + isbn +" found"}), 422
    isbn_id = isbn_id[0]
    select = "SELECT isbn, title, author, year, COUNT(*), AVG(rate)::numeric(10,2) FROM reviews JOIN books ON books.id = reviews.isbn_id WHERE isbn_id = :isbn_id GROUP BY books.id"
    reviews = db.execute(select, {"isbn_id":isbn_id}).fetchone()
    
    if reviews is None:

        select = "SELECT * FROM books WHERE id = :isbn"
        alter = db.execute(select, {"isbn":isbn_id}).fetchone() 
        return jsonify({
            "title":alter.title,
            "author":alter.author,
            "year":alter.year,
            "isbn":alter.isbn,
            "count":0,
            "average":0
        })

    return  jsonify({
        "title":reviews.title,
        "author":reviews.author,
        "year":reviews.year,
        "isbn":reviews.isbn,
        "count":reviews.count,
        "average":reviews.avg
    })
    
def goodread(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
    params={"key": "4qQ33gRusyHcS7NP277GQ", "isbns": isbn})

    if res.status_code != 200:
        raise Exception("Error: API request unsuccessful.")
    data = res.json()
    rate = data["books"][0]["work_ratings_count"]
    return rate
