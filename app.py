# Import the dependencies.
import numpy as np
import datetime as dt 
from datetime import timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine('sqlite://Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.measurment
measurement = Base.classes.measurement
# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################

app = Flask(__name__)

most_recent_date = session.query(func.max(measurement.date)).scalar()
#################################################
# Flask Routes
#################################################
@app.route("/")
def route_lists():
    return (f'Available Routes:<br/>'
        f'/api/v1.0/precipitation'
        f'/api/v1.0/stations'
        f'/api/v1.0/tobs'
        f'("/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end>'
    )
    

@app.route("/api/v1.0/precipitation")
def prec_query():
    from datetime import timedelta
    most_recent_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago =  most_recent_date - timedelta(days=365)
    prcp_query = session.query(measurement.date, func.Max(measurement.prcp))\
    .filter(measurement.date >= one_year_ago)
    dict = {"date": most_recent_date,
            "prcp": prcp_query

    }
    return dict.json()


@app.route("/api/v1.0/stations")
def station_list():
    station_query = session.query(station.station)
    return station_query.json()



@app.route("/api/v1.0/tobs")
def temps():
    
    most_active_station = "U"
    one_year_ago =  most_recent_date - timedelta(days=365)
    temp_ob_q = session.query(measurement.date, measurement.tobs)
    filter(measurement.station == most_active_station, measurement.date >= one_year_ago).all()
    return temp_ob_q.json()


@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def stats():
    most_active_station = "U"
    stats =session.query(func.min(measurement.tobs),
                                func.max(measurement.tobs),
                                func.avg(measurement.tobs)).\
                            filter(measurement.station == most_active_station).all()
    return














####Run the code
if __name__ == '__main__':
    app.run()