import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
Session(app)

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

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return redirect(url_for('index'))
    session.pop('user_id', None)
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "ismail":
        if password == "ismail":
            session['user_id'] = 1
            return  redirect(url_for('profile'))
        return redirect(url_for('index'))
    return render_template('book/index.html')

@app.route("/profile", methods=["GET"])
def profile():

    return render_template('book/profile.html', isbn=isbn.author)

