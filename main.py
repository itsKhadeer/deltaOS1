from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List, Annotated
import mysql.connector

app = FastAPI()

# Database connection setup
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Khan@2004",
    "database": "deltaos1"
}

db_conn = mysql.connector.connect(**db_config)
db_cursor = db_conn.cursor(dictionary=True)






# Define models
class Airport(BaseModel):
    id: int
    name: str
    location: str

class Flight(BaseModel):
    id: int
    name: str
    departure_airport: Airport
    arrival_airport: Airport
    departure_time: int
    arrival_time: int



# Endpoint to get flights at a specific airport on a given day
@app.get("/airport/{airport_id}")
def get_flights_at_airport(airport_id: int, ):
    query = "SELECT name FROM Flights WHERE departure_airport_id = %s OR arrival_airport_id = %s"
    db_cursor.execute(query, (airport_id, airport_id))
    flights = db_cursor.fetchall()
    if(flights):
        return flights
    else :
        raise HTTPException(status_code=404, detail="airport_id not found")


# Endpoint to find the next flight for a given time and destination
class location(str, Enum):
    Location1 = "Location 1"
    Location2 = "Location 2"
    Location3 = "Location 3"
    Location4 = "Location 4"
    Location5 = "Location 5"
    Location6 = "Location 6"
    Location7 = "Location 7"
    Location8 = "Location 8"
    Location9 = "Location 9"
    Location10 = "Location 10"
    Location11 = "Location 11"

@app.get("/nextFlight/{time}/{destination}")
def get_next_flight(time: int, destination: location):

    if(time > 24 or time < 0) :
        raise HTTPException(status_code=400, detail="invalid time input")
    
    querry = "select * from flights where departure_time > %s and arrival_airport_id = (select id from airports where location = %s)"
    db_cursor.execute(querry, (time,destination))
    next_flight = db_cursor.fetchall()
    if next_flight:
        return next_flight
    else :
        return f"no flights going to {destination} available after {time} hours today"
    


# Endpoint to find the busiest airport at a given hour
@app.get("/busiest/{time}")
def get_busiest_airport(time: int):

    busiest_airport = 0
    return busiest_airport
    
# Close the database connection after request
@app.on_event("shutdown")
def shutdown_db_conn():
    db_cursor.close()
    db_conn.close()
