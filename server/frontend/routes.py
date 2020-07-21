from . import app
from flask import Response, request, render_template, abort
from .models import Sensor, Experiment, Point

import json
import time

DATA_LOOP_INTERVAL = 1.0

@app.route('/sensor/<name>', methods=['GET'])
def sensor(name=None):
    return render_template('sensor.html', name=name)

@app.route('/sensor/data/<name>', methods=['GET'])
def sensor_data(name=None):
    with app.app_context():
        return Response(data_update(name), mimetype='text/event-stream')

@app.route('/')
def hello_world():
    return 'Hello, World!'

def data_update(name):
    points = []
    sensor = Sensor.query.filter_by(name=name).first()
    if sensor: 
        points = sensor.points
    else: abort(404)

    prev_data = None

    yield f"data:{json.dumps({'reset': True})}\n\n"
    
    data = list(map(lambda point: {'data': point.data, 'timestamp': str(point.time)}, points))
    for point in data:
        prev_data = point
        yield f"data:{json.dumps(point)}\n\n"

    while True:
        try:
            sensor = Sensor.query.filter_by(name=name).first()
            points = sensor.points

            data = list(map(lambda point: {'data': point.data, 'timestamp': str(point.time)}, points))[-1]
            if prev_data == data: continue

            yield f"data:{json.dumps(data)}\n\n"
            time.sleep(DATA_LOOP_INTERVAL)
        except IndexError:
            pass
