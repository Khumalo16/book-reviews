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
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


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

    return render_template('book/profile.html')

