from flask import Flask, jsonify

import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)

@app.route('/')
def index():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"api/v1.0/tobs<br/>"
        f"api/v1.0/<start><br/>"
        f"api/v1.0/<start>/<end><br/>"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    """"""
    return dict()
@app.route('/api/v1.0/stations')
def stations():
    """"""
    return jsonify()
@app.route('api/v1.0/tobs')
def tobs():
    """"""
    return jsonify()
@app.route('api/v1.0/<start>')
def temps_from():
    """"""
    return jsonify()
@app.route('api/v1.0/<start>/<end><br/>')
def temps_between():
    """"""
    return jsonify()
if __name__ == '__main__':
    app.run(debug=True)