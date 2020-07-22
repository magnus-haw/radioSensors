from . import app, db
from flask import Response, request, render_template, abort, redirect, url_for, g
from .models import Sensor, Experiment, Point

import json
import time

DATA_LOOP_INTERVAL = 1.0

@app.route('/', methods=['GET'])
def index():
    experiments = Experiment.query.all()
    sensors = Sensor.query.all()
    return render_template('index.html', experiments=experiments, sensors=sensors)

@app.route('/create-experiment', methods=['POST'])
def create_experiment():
    name = request.form['experiment-name']
    description = request.form['experiment-desc']
    existing = Experiment.query.filter_by(name=name).first()

    if existing: pass
    else:
        experiment = Experiment(name=name, description=description)
        db.session.add(experiment)
        db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete-experiment/<experiment_id>', methods=['POST'])
def delete_experiment(experiment_id):
    experiment = Experiment.query.filter_by(id=experiment_id).first()
    db.session.delete(experiment)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/sensor/<name>', methods=['GET'])
def sensor(name=None):
    return render_template('sensor.html', name=name)

@app.route('/sensor/data/<name>', methods=['GET'])
def sensor_data(name=None):
    return Response(data_update(name), mimetype='text/event-stream')

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
