import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from . import db

# Defining a schema for each category 

class Sensor(db.Model):
    __tablename__ = 'sensor'
    id              = db.Column(db.Integer,       primary_key=True)
    name            = db.Column(db.String,        nullable=False)
    description     = db.Column(db.String,        nullable=True)

    def __repr__(self):
        return '<Sensor id=%i, name=%s, description=%s>'%(self.id, self.name, self.description)

class Calibration(db.Model):
    id              = db.Column(db.Integer,       primary_key=True)
    type            = db.Column(db.String(50),    nullable=False)
    timestamp       = db.Column(db.DateTime,      nullable=False,    default=datetime.datetime.utcnow)
    expires         = db.Column(db.DateTime,      nullable=False,    default=datetime.datetime.utcnow)
    a1              = db.Column(db.Float,         nullable=False)
    a2              = db.Column(db.Float,         nullable=False)
    a3              = db.Column(db.Float,         nullable=False)
    a4              = db.Column(db.Float,         nullable=False)
    sensor_id       = db.Column(db.Integer,       db.ForeignKey('sensor.id'), nullable=False)
    sensor          = db.relationship("Sensor",   backref=db.backref('calibrations', lazy=True))

    def __repr__(self):
        return '<Calibration id=%i, type=%s, timestamp=%s, expires=%s, a1=%f, a2=%f, a3=%f, a4=%f, sensor_id=%i>' \
    %(self.id, self.type, self.timestamp, self.expires, self.a1, self.a2, self.a3, self.a4, self.sensor_id)

class Experiment(db.Model):
    id              = db.Column(db.Integer,       primary_key=True)
    name            = db.Column(db.String,        nullable=False)
    description     = db.Column(db.String,        nullable=True)
    
    def __repr__(self):
        return '<Experiment id=%i, name=%s, description=%s>'%(self.id, self.name, self.description)

class Point(db.Model):
    id              = db.Column(db.Integer,       nullable=False,    primary_key=True)
    data            = db.Column(db.Float,         nullable=False)
    time            = db.Column(db.DateTime,      nullable=False,    default=datetime.datetime.utcnow)
    sensor_id       = db.Column(db.Integer,       db.ForeignKey('sensor.id'),  nullable=False,    )
    sensor          = db.relationship("Sensor",   backref=db.backref('points', lazy=True))

    experiment_id   = db.Column(db.Integer,       db.ForeignKey('experiment.id'),nullable=False,    )
    experiment      = db.relationship("Experiment", backref=db.backref('points', lazy=True))

    def as_dict(self):
        result = {getattr(self, col.name) for col in self.__table__.columns}
        return result
   
    def __repr__(self):
        return '<Point id=%i, data=%f, time=%s, sensor_id=%i, experiment_id=%i>' \
    %(self.id, self.data, self.time, self.sensor_id, self.experiment_id)

