import os

from flask import Flask, session, render_template, request, redirect, url_for,flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
Session(app)

user = 0
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgresql://hhlfjdydmhizma:f2137338537e4dd691d12095ab2abf893b8bfca7b2b72d74a260c27367a6111a@ec2-54-144-196-35.compute-1.amazonaws.com:5432/d4edp75p3661vk")
db = scoped_session(sessionmaker(bind=engine))

isbn = db.execute("SELECT id, isbn, title,author, year FROM books WHERE id = 2").fetchone()
@app.route("/")
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
    
    if password != confirm:
        flash("Password does not match")
    try:
        db.execute("INSERT INTO users (name, surname, username, password) VALUES (:name, :surname, :username, :password)",
                    {"name":name, "surname": surname, "username": username, "password": password})
        db.commit()

        select = "SELECT id FROM users WHERE username = :username"
        user_id = db.execute(select,{"username": username}).fetchone()
        session["user_id"] = user_id

    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        flash("The username already exists!")
    flash("You are successful registered in Books reviews website!")
    return  redirect(url_for('index'))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return redirect(url_for('index'))

    username = request.form.get("username")
    password = request.form.get("password")
    select = "SELECT * FROM users WHERE username = :username AND password = :password"

    if db.execute(select,{"username": username, "password": password}).rowcount == 0:
        return redirect(url_for('index'))

    select = "SELECT id FROM users WHERE username = :username"
    user_id = db.execute(select,{"username": username}).fetchone()
    session["user_id"] = user_id
    user = user_id

    return render_template('book/profile.html')

@app.route("/profile", methods=["GET"])
def profile():

    if "user" in session:
        return render_template('book/profile.html', isbn=isbn.year)
    return redirect(url_for('index'))

