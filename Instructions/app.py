import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print (Base.classes.keys())

# Save reference to the table
measurement= Base.classes.measurement
station= Base.classes.station

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
        f"/api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/percipitation")
def percip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers 
    #results = session.query(measurement.date).all()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results=session.query(measurement.date,measurement.prcp).filter(measurement.date >= query_date).all()
    session.close()

    # Convert list of tuples into normal list
    results2= list(np.ravel(results))

    return jsonify(results2)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    
    station_list = session.query(station.id,station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    
    station_list2= list(np.ravel(station_list))
    return jsonify(station_list2)
    session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    
    tobs_list=session.query(measurement.tobs,measurement.date).filter(measurement.station=='USC00519281')\
    .filter(measurement.date>='2016-08-23').all()
    
    
    # session.query(measurement.date,measurement.tobs).filter(measurement.station =="USC00519281").all()
    
    tobs_list2= list(np.ravel(tobs_list))
    return jsonify(tobs_list2)
    session.close()


@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    if not end:   
        start1= session.query(func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date >= start)).all()
   
        session.close()
        
        start2= list(np.ravel(start1))
        return jsonify(start2)
    
    
    start_end= session.query(func.max(measurement.tobs),func.min(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date >= start).filter(measurement.date <=end)).all() 

    session.close()
    start3= list(np.ravel(start_end))
    return jsonify(start3)

 
 

if __name__ == '__main__':
    app.run(debug=True)
