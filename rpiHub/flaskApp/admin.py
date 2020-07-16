from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask import current_app as app
from . import db
from .models import Sensor, Experiment, Calibration, Point

admin = Admin(app, name='RadioSensors', template_mode='bootstrap3')
admin.add_view(ModelView(Sensor, db.session))
admin.add_view(ModelView(Experiment, db.session))
admin.add_view(ModelView(Calibration, db.session))
admin.add_view(ModelView(Point, db.session))
