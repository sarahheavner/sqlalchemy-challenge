#Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt


#Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask setup
app = Flask(__name__)

#Set Flask Routes
@app.route('/')
def home():
    """list all available API routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route('/api/v1.0/precipitation')  
def precipitation():
    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    session = Session(engine)

    precip = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_precip = []
    for date, prcp in precip:
        precip_dict={}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)



@app.route('/api/v1.0/stations')
def stations():
    """Return a JSON list of stations from the dataset."""
    session = Session(engine)
    
    results = session.query(Station.station, Station.name).all()

    session.close()

    all_stations = []
    for station, name in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route('/api/v1.0/tobs')
def tobs():
    """Query the dates and temperature observations of the most active station for the last year of data."""
    session = Session(engine)

    #Find most active station
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()
    (most_active, ) = most_active_station

    #Find date range
    recent_date_most_active = session.query(Measurement.date).filter(Measurement.station == most_active).order_by(Measurement.date.desc()).first()
    (most_recent_date, ) = recent_date_most_active

    most_recent_date = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    most_recent_date = most_recent_date.date()
    twelve_months =  most_recent_date - dt.timedelta(days=365)

    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= twelve_months).all()

    session.close()

    all_tobserv = []
    for date, tobs in all_tobserv:
        all_tobserv_dict = {}
        all_tobserv_dict['date'] = date
        all_tobserv_dict['tobs'] = tobs
        all_tobserv.append(all_tobserv_dict)

    return jsonify(all_tobserv)


@app.route('/api/v1.0/start')
def start():

    session = Session(engine)





if __name__ == '__main__':
    app.run(debug=True)