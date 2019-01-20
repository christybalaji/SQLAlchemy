# Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify
import numpy as np

# Create an engine to a SQLite database file called `hawaii.sqlite`
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



# # Dictionary of Justice League
# justice_league_members = [
#     {"superhero": "Aquaman", "real_name": "Arthur Curry"},
#     {"superhero": "Batman", "real_name": "Bruce Wayne"},
#     {"superhero": "Cyborg", "real_name": "Victor Stone"},
#     {"superhero": "Flash", "real_name": "Barry Allen"},
#     {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
#     {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
#     {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
# ]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and prcp information from the last year """
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    
    # Create a dictionary from the row data and append to a list
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)

    return jsonify(precipitation_values)


@app.route("/api/v1.0/stations")
def stations():
    """Return the justice league data as json"""
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs=session.query(Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").\
    filter(Measurement.station == "USC00519281").all()

    temps = list(np.ravel(tobs))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    if end != None:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
            
    temps = list(np.ravel(results))
    return jsonify(temps)



@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/\"startdate yyyy-mm-dd\"<start><br/>"
        f"/api/v1.0/temp/\"startdate as yyyy-mm-dd\"/\"enddate as yyyy-mm-dd\"<br/><br/>"
         
    )


if __name__ == "__main__":
    app.run(debug=True)
