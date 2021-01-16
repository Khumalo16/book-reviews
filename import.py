
import csv
import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)
Session(app)

# Check for environment variable
if not os.getenv("postgres://hhlfjdydmhizma:f2137338537e4dd691d12095ab2abf893b8bfca7b2b72d74a260c27367a6111a@ec2-54-144-196-35.compute-1.amazonaws.com:5432/d4edp75p3661vk"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("book.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()

if __name__ == "__main__":
    main()