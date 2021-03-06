from . import app, db
from flask import Response, request, render_template, abort, redirect, url_for, session
from .models import Sensor, Experiment, Point

import json
import time
import threading

DATA_LOOP_INTERVAL = 1.0

from .radio import RadioBonnet
radio_instance = RadioBonnet()
sensor_thread = threading.Thread(target=radio_instance.listen)
sensor_thread.start()

@app.route('/', methods=['GET'])
def index():
    experiments = Experiment.query.order_by(Experiment.id.desc()).all()
    sensors = Sensor.query.all()
    return render_template('index.html', 
        experiments=experiments, 
        sensors=sensors,
        active_experiment=radio_instance.get_experiment(),
        active_sensors=radio_instance.active
    )

@app.route('/start-experiment/<experiment_id>', methods=['POST'])
def start_experiment(experiment_id):
    experiment = Experiment.query.filter_by(id=experiment_id).first()
    radio_instance.set_experiment(experiment)
    return redirect(url_for('index'))

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
    sensor = Sensor.query.filter_by(name=name).first()
    return render_template('sensor.html', sensor=sensor)

@app.route('/sensor/data/<name>', methods=['GET'])
def sensor_data(name=None):
    return Response(data_update(name), mimetype='text/event-stream')

def data_update(name):
    while True:
        try:
            sensor = Sensor.query.filter_by(name=name).first()
            point = Point.query.filter_by(sensor=sensor).order_by(Point.time.desc()).first()
            data = {'data': point.data, 'timestamp': str(point.time)}

            yield f"data:{json.dumps(data)}\n\n"
            time.sleep(DATA_LOOP_INTERVAL)
        except IndexError:
            pass
