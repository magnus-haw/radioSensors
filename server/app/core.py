import datetime
import time
import json
from flask import Flask, Response, request, render_template
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.insert(1, '../sensor')
from sensor import Sensor

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RADIO_SENSOR_DB'] # for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DATA_LOOP_INTERVAL = 1.0

db = SQLAlchemy(app)

import model

@app.route("/")
def show_data():
    return str(model.list())

@app.route("/stream")
def stream_data():
    def data_loop():
        while True:
            try:
                json_data = json.dumps(model.list()[-1])
                yield f"data:{json_data}\n\n"
                time.sleep(DATA_LOOP_INTERVAL)
            except IndexError:
                pass
    return Response(data_loop(), mimetype='text/event-stream')

@app.route("/realtime")
def realtime_chart():
    return render_template('realtime.html')

@app.route("/temperature", methods=["POST"])
def insert_data():
    model.add_data(request.get_json())
    return "OK"

if __name__ == "__main__":
    app.run(debug=True, port=80, host='0.0.0.0')

    
