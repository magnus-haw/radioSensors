import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from flask import redirect
from flask_restful import Resource, reqparse
from .core import api, db, app

class SensorData(db.Model):
    id          = Column(Integer,       nullable=False, primary_key=True)
    therm_data  = Column(Float,         nullabe=False)
    timestamp   = Column(DateTime,      nullabe=False, default=datetime.datetime)

def as_dict(self):
    result = {getattr(self, col.name) for col in self.__table__.columns}
    return result

def add_data(data):
    db.session.add(data)
    db.session.commit()

def list():
    return SensorData.query.all()

class SensorDataEndpoint(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('therm_data', type=float, required=True)
    
    def post(self):
        args = self.parser.parse_args()
        add_data(SensorData(**args))
        return {"status": "ok"}

class ListEndpoint(Resource):
    def get(self):
        return list()

api.add_resource(SensorDataEndpoint, '/sensor_data/add')
api.add_resource(ListEndpoint, '/sensor_data/list')
