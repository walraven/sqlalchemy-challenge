from flask import Flask, jsonify

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#flask setup
app = Flask(__name__)

@app.route('/')
def index():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    """Returns the jsonified prcp data for the last year in the database
    as a list of dictionaries with the date as key and prcp as val"""
    
    #begin session
    session = Session(engine)

    #query for most recent date and then calculate date 1 year prior
    max_date_str = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()[0]
    max_date_dt = dt.datetime.strptime(max_date_str, '%Y-%m-%d').date()
    low_bound_dt = max_date_dt.replace(year=(max_date_dt.year - 1))
    low_bound_str = low_bound_dt.strftime('%Y-%m-%d')

    #query the data
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > low_bound_str)

    #no more quereies
    session.close()

    #initialize return object
    return_list = []

    #convert results into list of dictionaries
    for row in results:
        prcp_dict = {row[0]:row[1]}
        return_list.append(prcp_dict)

    #we're done here
    return jsonify(return_list)

@app.route('/api/v1.0/stations')
def stations():
    """Returns jsonified data of all of the stations in the database"""
    
    #start the session
    session = Session(engine)

    #perform the query
    results = session.query(Station.station,Station.name,\
        Station.latitude,Station.longitude,Station.elevation).all()
    
    #lock it up!
    session.close()

    #initialize return object
    stations = []

    #populate object
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        stations.append(station_dict)
    
    #that's all, folks!
    return jsonify(stations)

@app.route('/api/v1.0/tobs')
def tobs():
    """Returns jsonified data for the most active station for the last
     year of data"""
    
    #open session-e
    session = Session(engine)

    #determine most active station
    station_id = session.query(Measurement.station,\
        func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc()).first()[0]

    #determine most recent observation
    max_date_str = session.query(Measurement.date).\
        filter(Measurement.station == station_id).\
        order_by(Measurement.date.desc()).first()[0]

    #determine date 1 year prior
    max_date_dt = dt.datetime.strptime(max_date_str, '%Y-%m-%d').date()
    low_bound_dt = max_date_dt.replace(year=(max_date_dt.year - 1))
    low_bound_str = low_bound_dt.strftime('%Y-%m-%d')

    #perform query
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > low_bound_str,\
        Measurement.station == station_id)

    #no more queries
    session.close()

    #initialize return obj
    temps = []

    #populate return obj
    for date, temp, in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temp'] = temp
        temps.append(temp_dict)

    #it's your turn to return
    return jsonify(temps)

@app.route('/api/v1.0/<start>')
def temps_from(start):
    """Returns the min, max, and avg temperatures calculated from the
    given start date to the end of the dataset"""

    #let us begin
    session = Session(engine)

    #the query
    results = session.query(Measurement.date,\
        func.min(Measurement.tobs),func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date)

    #let us end
    session.close()

    #initialize return object
    dates = []

    #populate the object    
    for date, min, max, avg in results:
        date_dict = {}
        date_dict['date'] = date
        date_dict['min'] = min
        date_dict['max'] = max
        date_dict['avg'] = avg
        dates.append(date_dict)

    #let us leave
    return jsonify(dates)

@app.route('/api/v1.0/<start>/<end>')
def temps_between(start,end):
    """Returns the min, max, and avg temperatures calculated from the 
    given start date to the given end date"""

    #start it up!
    session = Session(engine)

    #get the date, the min, max, and average, but only for the dates provided
    results = session.query(Measurement.date,\
        func.min(Measurement.tobs),func.max(Measurement.tobs),\
        func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).\
        group_by(Measurement.date)

    #shut it down!
    session.close()

    #initialize return object
    dates = []

    #get it together
    for date, min, max, avg in results:
        date_dict = {}
        date_dict['date'] = date
        date_dict['min'] = min
        date_dict['max'] = max
        date_dict['avg'] = avg
        dates.append(date_dict)

    #make like a tree...
    return jsonify(dates)


if __name__ == '__main__':
    app.run(debug=True)