import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine(r"sqlite:///C:\Users\sooki\OneDrive\Desktop\Bootcamp Classwork Projects\Week 10 - SQL Alchemy\sqlalchemy_challenge\Starter_Code\Resources\hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>" 
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-24").\
        all()
    
    session.close()

    # Convert the query results to a dictionary
    # By using date as the key and prcp as the value
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(station.station).\
                order_by(station.station).all()

    session.close()

    # Return a JSON list of stations from the dataset.
    station_list = [result[0] for result in results]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all TOBs"""
    # Query the dates and temperature observations of the most-active station
    # For the previous year of data.
    results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
                filter(measurement.date >= '2016-08-23').\
                filter(measurement.station=='USC00519281').\
                order_by(measurement.date).all()

    session.close()

    # Return a JSON list of temperature observations for the previous year.
    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the maximum temperature for a start date"""
    # Query all tobs
    results = session.query(func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                            filter(measurement.date >= start_date).all()

    session.close()

    # Create a dictionary and return a JSON list
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 

    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of the minimum temperature, the average temperature, and the maximum temperature for a start-end range"""
    # Query all tobs
    results = session.query(func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                            filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()

    # Create a dictionary and return a JSON list
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    
    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)
