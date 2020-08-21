from . import app, db
from flask import Response, request, render_template, abort, redirect, url_for, session
from .radio import RadioBonnet
from .models import Point

@app.route('/')
def hello_world():
    return 'Hello, World!'
