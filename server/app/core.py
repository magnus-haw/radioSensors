import datetime
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sensor import Sensor
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RADIO_SENSOR_DB'] # for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

import model

@app.route("/")
def show_data():
    return str(model.list())

@app.route("/temperature", methods=["POST"])
def insert_data():
    model.add_data(request.get_json())
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')

    
