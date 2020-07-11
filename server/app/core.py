import datetime
import time
import json
from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RADIO_SENSOR_DB'] # for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DATA_LOOP_INTERVAL = 1.0

db = SQLAlchemy(app)

import model

# List all data
@app.route("/list")
def show_all_data():
    return str(model.list())

# List all data sent by the sensor
@app.route("/list/sensor/<name>")
def show_sensor_data(name):
    return str(model.list(by='sensor', name=name))

# List all data belonging to the experiment
@app.route("/list/experiment/<name>")
def show_experiment_data(name):
    return str(model.list(by='experiment', name=name))

# Data streaming endpoint
@app.route("/stream/<experiment>/<sensor>")
def stream_data():
    def data_loop():
        while True:
            try:
                data = model.list()[-1]
                json_data = json.dumps(data)
                yield f"data:{json_data}\n\n"
                time.sleep(DATA_LOOP_INTERVAL)
            except IndexError:
                pass
    return Response(data_loop(), mimetype='text/event-stream')

# Realtime data visualization
@app.route("/realtime")
def realtime_chart():
    return render_template('realtime.html')

# Post data
@app.route("/data", methods=["POST"])
def insert_data(experiment, sensor):
    for data in request.get_json():
        model.add_data(data['experiment'], data['sensor'], data['value'])
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')

    
