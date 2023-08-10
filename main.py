from fastapi import FastAPI, HTTPException
from enum import Enum
from datetime import datetime;
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



# Endpoint to get flights at a specific airport on a given day
@app.get("/airport/{airport_id}")
def get_flights_at_airport(airport_id: int, ):
    query = "SELECT * FROM Flights WHERE departure_airport_id = %s OR arrival_airport_id = %s"
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




@app.get("/nextFlight/{time}/{destination}")
def get_next_flight(time: datetime, destination: location):

    if(time.hour > 24 or time.hour < 0) :
        raise HTTPException(status_code=400, detail="invalid time input")
    
    querry = "select * from flights where departure_time > %s and arrival_airport_id = (select id from airports where location = %s)"
    db_cursor.execute(querry, (time,destination))
    next_flight = db_cursor.fetchall()
    if next_flight:
        return next_flight
    
    else :
        return f"no flights going to {destination} available after {time.time} hours today"
    



# Endpoint to find the busiest airport at a given hour
@app.get("/busiest/{time}")
def get_busiest_airport(time: int):

    querry = "select departure_airport_id from flights where hour(departure_time) = %s"
    db_cursor.execute(querry, (time,))
    the_table = db_cursor.fetchall()
    print(the_table)
    frequency_dict = {}
    for rows in the_table: 

        if rows["departure_airport_id"] in frequency_dict.keys() :
            frequency_dict[rows["departure_airport_id"]] += 1
        
        else : 
            frequency_dict[rows["departure_airport_id"]] = 1
    print(frequency_dict)

    querry = "select arrival_airport_id from flights where hour(arrival_time) = %s"
    db_cursor.execute(querry, (time,))
    the_table = db_cursor.fetchall()
    
    for rows in the_table: 

        if rows["arrival_airport_id"] in frequency_dict.keys() :
            frequency_dict[rows["arrival_airport_id"]] += 1
        
        else : 
            frequency_dict[rows["arrival_airport_id"]] = 1
    
    if frequency_dict:
        max_val = sorted(frequency_dict.values(), reverse=True)
        Keymax = max_val[0]
        print(frequency_dict)
        querry="select name,location from airports where id = %s"
        db_cursor.execute(querry,(Keymax,))
        return db_cursor.fetchall()
    return "there are no flights landing or taking off at the given hour in any airport"
            
        
# Close the database connection after request
@app.on_event("shutdown")
def shutdown_db_conn():
    db_cursor.close()
    db_conn.close()
