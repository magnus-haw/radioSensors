from flask import render_template, current_app as app
from . import db

@app.route('/<name>')
def sensor(name=None,temp=None):
    temp = 75 ###acquire temperature measurement here
    return render_template('sensor.html', name=name, temp=temp)

@app.route('/')
def hello_world():
    return 'Hello, World!'

