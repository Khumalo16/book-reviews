
#import csv
import os, requests

from flask import Flask, session, jsonify
#from flask_session import Session
#rom sqlalchemy import create_engine
#rom sqlalchemy.orm import scoped_session, sessionmaker


#app = Flask(__name__)
#Session(app)

# Check for environment variable


# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# Set up database
#engine = create_engine(("postgres://hhlfjdydmhizma:f2137338537e4dd691d12095ab2abf893b8bfca7b2b72d74a260c27367a6111a@ec2-54-144-196-35.compute-1.amazonaws.com:5432/d4edp75p3661vk"))
#db = scoped_session(sessionmaker(bind=engine))


def main():
   # f = open("books.csv")
   # reader = csv.reader(f)
   # for isbn, title, author, year in reader:
   #     db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
   #     {"isbn": isbn, "title": title, "author": author, "year": year})
   #     db.commit()
   isbn = "1416528636"
   res = requests.get("https://www.goodreads.com/book/review_counts.json",
   params={"key": "11lde3d29lqXUBzAdHwQ", "isbns": isbn})

   if res.status_code != 200:
      raise Exception("Error: API request unsuccessful.")
   data = res.json()
   rate = data["books"][0]["work_ratings_count"]
   print(rate)


if __name__ == "__main__":
    main()
   