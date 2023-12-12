# Assignment 10 - Part 2
#API SQLite Connection & Landing Page

# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy import create_engine, text,inspect,func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base


#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
# engine = create_engine("sqlite://C:/Assignment 10 -sqlalchemy challenge/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite", echo=False,connect_args={"check_same_thread": False})
engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False,connect_args={"check_same_thread": False})
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)
Base.classes.keys()

# Save references to each table
Measurement =Base.classes.measurement
Station =Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask,jsonify
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Display the available routes on the landing page

@app.route("/")

def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipiations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# A precipitation route that:
#the date as the key and the value as the precipitation 
#Only returns the jsonified precipitation data for the last year in the database 
@app.route("/api/v1.0/precipiations")

def precipitation():
    
        year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        perci = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>= year_ago).all()
        precip = dict(perci)
        return jsonify(precip)
# A stations route that:
@app.route("/api/v1.0/stations")
#Returns jsonified data of all of the stations in the database   
def station():
    
        all_station = session.query(Measurement.station).group_by(Measurement.station).all() 
        # Convert list of tuples into normal list
        station_names = list(np.ravel(all_station))
        return jsonify(station_names)
#A tobs route that:
@app.route("/api/v1.0/tobs")
#Returns jsonified data for the most active station (USC00519281) 
def tob():
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    temp_observation = session.query(Measurement.date,Measurement.tobs). filter(Measurement.station == 'USC00519281').\
                   filter(Measurement.date >= year_ago).all()
    # temp = list(np.ravel(temp_observation))
    temp = dict(temp_observation)
    return jsonify(temp)

#Only returns the jsonified data for the last year of data 
# API Dynamic Route
#A start route that:
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
#Accepts the start date as a parameter from the URL and deliver the min, max, ave temperature after the date entered
def start_date(start, end = None):
    agr_temp_values = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs)))
    if start:
        start = dt.datetime.strptime(start, "%Y%m%d") 
        agr_temp_values  = agr_temp_values.filter(Measurement.date >= start)
    # To check if there is an end value or not
    if end: 
        end = dt.datetime.strptime(end, "%Y%m%d")
        agr_temp_values  = agr_temp_values.filter(Measurement.date <= end)
    # session.close()
    # Convert the results in to a dictionary
    results = agr_temp_values.all()[0]
    session.close()
    key = ["Min Temp","Max Temp","Ave Temp"]
    temp_dict = {key[i]:results[i] for i in range(len(key))}
    return jsonify(temp_dict)
      
if __name__ == "__main__":
    app.run(debug=True)