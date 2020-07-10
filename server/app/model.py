import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from flask_restful import reqparse
from core import db

# Defining a schema for all sensor data
# class SensorData(db.Model):
#     id          = Column(Integer,       nullable=False, primary_key=True)
#     data_type   = Column(String,        nullable=False)
#     data        = Column(Float,         nullable=False)
#     timestamp   = Column(DateTime,      nullable=False, default=datetime.datetime.utcnow)

# Defining a schema for each category of sensor data
class TempData(db.Model):
    id          = Column(Integer,       nullable=False, primary_key=True)
    data        = Column(Float,         nullable=False)
    timestamp   = Column(DateTime,      nullable=False, default=datetime.datetime.utcnow())

    def as_dict(self):
        result = {getattr(self, col.name) for col in self.__table__.columns}
        return result

def add_data(data):
    db.session.add(TempData(data=data['data']))
    db.session.commit()

def list():
    return [x.as_dict() for x in TempData.query.all()]

db.create_all()
db.session.commit()