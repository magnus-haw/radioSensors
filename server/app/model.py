import datetime
import itertools
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_restful import reqparse
from core import db

class Experiment(db.Model):
    __tablename__ = 'experiment'
    id              = Column(Integer,       primary_key=True)
    name            = Column(String,        nullable=False)
    sensors         = relationship("Sensor", back_populates="experiment", lazy=True)

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id              = Column(Integer,       primary_key=True)
    name            = Column(String,        nullable=False)
    experiment_id   = Column(Integer,       ForeignKey('experiment.id'))
    experiment      = relationship("Experiment", back_populates="sensors")
    points          = relationship("Point", back_populates="sensor", lazy=True)

class Point(db.Model):
    __tablename__ = 'point'
    id              = Column(Integer,       primary_key=True)
    sensor_id       = Column(Integer,       ForeignKey('sensor.id'))
    value           = Column(Float,         nullable=False)
    timestamp       = Column(DateTime,      nullable=False, default=datetime.datetime.utcnow())
    sensor          = relationship("Sensor", back_populates="points")

    def as_dict(self):
        return {c.name: jsonify(getattr(self, c.name)) for c in self.__table__.columns}

def add_experiment(experiment_name):
    experiment = Experiment(name=experiment_name)
    db.session.add(experiment)
    db.session.commit()

def add_sensor(experiment_name, sensor_name):
    experiment = Experiment.query.filter_by(name=experiment_name).first()
    if not experiment: raise ValueError('Experiment not found.')
    else:
        sensor = Sensor(experiment=experiment, name=sensor_name)
        experiment.sensors.append(sensor)
        db.session.add(sensor)
        db.session.commit()

def add_data(experiment_name, sensor_name, data):
    sensor = Sensor.query.filter_by(name=sensor_name).join(Sensor.experiment, aliased=True).filter_by(name=experiment_name).first()
    if not sensor: raise ValueError('Experiment or sensor not found.')
    else:
        point = Point(value=data['value'])
        sensor.points.append(point)
        db.session.add(point)
        db.session.commit()

def list(experiment_name, sensor_name):
    sensor = Sensor.query.filter_by(name=sensor_name).join(Sensor.experiment, aliased=True).filter_by(name=experiment_name).first()
    if not sensor: return []
    else: return [x.as_dict() for x in sensor.points]

db.create_all()
db.session.commit()

# Helpers
def jsonify(x):
    if type(x) is datetime.datetime:
        return str(x)

    return x

def get_class(tablename):
    for c in db.Model._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c