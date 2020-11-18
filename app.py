#Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


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
    #list all routes
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start_end<br/>'
    )


@app.route('/api/v1.0/precipitation')  
def precipitation():
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






if __name__ == '__main__':
    app.run(debug=True)