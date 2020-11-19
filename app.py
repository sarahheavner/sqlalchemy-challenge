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
#Create route to home
@app.route('/')
def home():
    """list all available API routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/start/&lt;start&gt;/&lt;end&gt;<br/>"
    )


#Create route for precipitation data
@app.route('/api/v1.0/precipitation')  
def precipitation():
    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    #Create session between Python and database
    session = Session(engine)

    #Query for date and precipitation measurement
    precip = session.query(Measurement.date, Measurement.prcp).all()

    #Close session
    session.close()

    #Create list / dictionary to store results
    all_precip = []
    for date, prcp in precip:
        precip_dict={}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        all_precip.append(precip_dict)

    #Return responses in JSON format
    return jsonify(all_precip)


#Create route for stations
@app.route('/api/v1.0/stations')
def stations():
    """Return a JSON list of stations from the dataset."""
    #Create session between Python and database
    session = Session(engine)

    #Query for station and name
    station_info = session.query(Station.station, Station.name).all()

    #Close session
    session.close()

    #Create list / dictionary to store results
    all_stations = []
    for station, name in station_info:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        all_stations.append(station_dict)

    #Return results in JSON format
    return jsonify(all_stations)


#Create route for tobs
@app.route('/api/v1.0/tobs')
def tobs():
    """Query the dates and temperature observations of the most active station for the last year of data."""
    #Create session between Python and database
    session = Session(engine)

    #Find most active station
    most_active_station = session.query(Measurement.station)\
                          .group_by(Measurement.station)\
                          .order_by(func.count().desc()).first()
    most_active = most_active_station[0]

    #Find most recent date and date 1 year ago for most active station
    recent_date_most_active = session.query(Measurement.date)\
                              .filter(Measurement.station == most_active)\
                              .order_by(Measurement.date.desc()).first()

    twelve_months = (dt.datetime.strptime(recent_date_most_active[0],'%Y-%m-%d') \
                   - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #Query for date and temperature using most active station and date range from above
    tobs = session.query(Measurement.date, Measurement.tobs)\
           .filter(Measurement.station == most_active)\
           .filter(Measurement.date >= twelve_months).all()
   
    #Close session
    session.close()

    #Create list / dictionary to store results
    all_tobserv = []
    for date, tobs in tobs:
        all_tobserv_dict = {}
        all_tobserv_dict['date'] = date
        all_tobserv_dict['tobs'] = tobs
        all_tobserv.append(all_tobserv_dict)

    #Return results in JSON format
    return jsonify(all_tobserv)#Create session between Python and database
    session = Session(engine)


    #Create route for TMIN, TAVG, and TMAX per date starting from a starting date
@app.route('/api/v1.0/<start>')
def start(start):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    #Create session between Python and database
    session = Session(engine)


    #Query for date, min, max, avg temperatures for given start date
    start_date_tobs = session.query(func.min(Measurement.tobs), \
                func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    #Close Session
    session.close()

    #Create list / dictionary for results
    min_avg_max_one = []
    for min, avg, max in start_date_tobs:
        min_avg_max_dict={}
        min_avg_max_dict['min'] = min
        min_avg_max_dict['avg'] = avg
        min_avg_max_dict['max'] = max
        min_avg_max_one.append(min_avg_max_dict)

    #Return results in JSON format
    return jsonify(min_avg_max_one)



#Create route for TMIN, TAVG, and TMAX per date between a date range
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    #Create session between Python and database
    session = Session(engine)

    #Query for date, min, max, avg temperatures for given start date
    start_end_date_tobs = session.query(func.min(Measurement.tobs)\
                ,func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                .filter(Measurement.date >= start)\
                .filter(Measurement.date <= end).all()

    #Close Session
    session.close()

    #Create list / dictionary for results
    min_avg_max = []
    for min, avg, max in start_end_date_tobs:
        min_avg_max_dict={}
        min_avg_max_dict['min'] = min
        min_avg_max_dict['avg'] = avg
        min_avg_max_dict['max'] = max
        min_avg_max.append(min_avg_max_dict)

    #Return results in JSON format
    return jsonify(min_avg_max)




if __name__ == '__main__':
    app.run(debug=True)