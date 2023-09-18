# Import the dependencies.
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import auto_map
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine= create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
base= automap_base()

# reflect the tables
base.prepare(autoload_with= engine)

# Save references to each table
measurement= base.classes.measurement
station= base.classes.station

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################
app= Flask(App)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Data Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
        previous_year= dt.date(2017, 8, 23) - dt.timedelta(days = 365)
        results= session.query(measurement.date, measurement.prcp).filter(measurement.date >= previous_year).all()
        session.close()
        precip= {date: prcp for date, prcp in precipitation}
        return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
        results= session.query(station.station).all()
        session.close()
        stations= list(np.ravel(results))
        return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
        previous_year= dt.date(2017, 8, 23) - dt.timedelta(days = 365)
        results= session.query(measurement.tobs).\
            filter(measurement.station== 'USC00519281').\
            filter(measurement.date>= previous_year).all()
        session.close()
        temp= list(np.ravel(results))
        return jsonify(temp)

@app.route("/api/v1.0/temp/start")
@app.route("/api/v1.0/temp/start/end")
def stats (start= None, end= None):
    sel= [(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))]
    if not end:
        start= dt.DateTime.strptime(start, "%D%M%Y")
        results= session.query(*sel).\
            filter (measurement.date>= start).all()
        session.close()
        tobs= list(np.ravel(results))
        return jsonify(tobs)
    
    start= dt.DateTime.strptime(start, "%D%M%Y")
    end= dt.DateTime.strptime(end, "%D%M%Y")
    results= session.query(*sel).\
            filter (measurement.date>= start).\
            filter (measurment.date<= end).all()
    session.close()
    tobs= list(np.ravel(results))
    return jsonify(tobs)

if __App__ == "__main__":
    app.run()
