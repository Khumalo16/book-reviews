import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
	comand = "SELECT origin, destination, duration FROM flights"
	flights = db.execute(comand).fetchall()
	for flight in flights:
		print(f"{flight.origin} to {flight.destination} : {fligth.duration}"

print(4)
