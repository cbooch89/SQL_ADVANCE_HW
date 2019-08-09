# import dependencies
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# <#################################################
# # Database Setup
# ################################################# -->
engine = create_engine("sqlite:///Hawaii.sqlite")

# reflect the database into a new model -->
Base = automap_base()
 # reflect the tables -->
Base.prepare(engine, reflect=True)

 # Save reference to the table -->
Station = Base.classes.station
Measurement = Base.classes.measurement

 # Create our session (link) from Python to the DB -->
session = Session(engine)

 #################################################
# Flask Setup
################################################# -->
app = Flask(__name__)

 #################################################
# Flask Routes
################################################# -->
@app.route("/")
def welcome():
    #  List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
 ################################################################################## -->

@app.route("/api/v1.0/precipitation")
def precipitation():

    session=Session(engine)

    rain = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > year_ago).order_by(Measurement.date).all()
    prcp_totals = []
    for result in rain:
        row = {}
        row["date"] = rain[0]
        row["prcp"] = rain[1]
        prcp_totals.append(row)
        session.close()
        return jsonify(prcp_totals)

 ################################################################################## -->

@app.route("/api/v1.0/stations")
def stations():
    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

 ################################################################################## -->

@app.route("/api/v1.0/tobs")
def tobs():
    
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    temp_info = session.query(Measurement.station, Measurement.tobs).\
                filter(Measurement.station == best_station).\
                filter(Measurement.date >= year_ago).all()

    # temp_totals = []
    # for result in temp_info:
    #     row = {}
    #     row["date"] = temp_info[0]
    #     row["tobs"] = temp_info[1]
    #     temp_totals.append(row)

    # return jsonify(temperature_totals)

    #  /api/v1.0/<start> and /api/v1.0/<start>/<end>

    #     Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
        
    #     When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
        
    #     When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive. 

if __name__ == "__main__":
    app.run(debug=True)