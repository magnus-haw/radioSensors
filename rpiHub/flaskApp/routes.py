from flask import render_template, current_app as app
from flask import flash, request, redirect, url_for
import threading
from flaskthreads import AppContextThread
from . import db
from .radio import RadioBonnet
from .forms import ExperimentForm
from .models import Experiment,Point,Sensor

# Instantiate RadioBonnet, thread, and lock
radio_instance = RadioBonnet()
dataLock = threading.Lock()

@app.route('/sensor/<name>')
def sensor(name=None,temp=None):
    sensor = Sensor.query.filter_by(name=name).first()
    temp = 75 ###acquire temperature measurement here
    return render_template('sensor.html', name=name, temp=temp)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/start-experiment/', methods=['GET','POST'])
def start_experiment():
    # Use radio object for interthread data storage
    global radio_instance

    # Create form object
    form = ExperimentForm(request.form)
    print(form.errors)

    # If form is being submitted
    if request.method == 'POST':
        name=request.form['name']
        description = request.form['description']
        print(name, description)

        # check if values are populated
        if form.validate():
            with dataLock:
                experiment = Experiment(name=name,description=description)
                db.session.add(experiment)
                db.session.commit()
                radio_instance.experiment_id = experiment.id
                radio_instance.stop = False
            sensor_thread = AppContextThread(target=radio_instance.listen)
            sensor_thread.start()

            flash('Started ' + name)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('ExperimentForm.html', form=form)

@app.route('/stop-experiment/', methods=['POST'])
def stop_experiment():
    # Use radio object for interthread data storage
    global radio_instance
    with dataLock:
        radio_instance.stop = True
 
    return redirect(url_for('start_experiment'))

