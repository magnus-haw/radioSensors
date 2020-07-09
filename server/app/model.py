import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from app import db

class SensorData(db.Model):
    id          = Column(Integer,       nullable=False, primary_key=True)
    data        = Column(Float,         nullabe=False)
    timestamp   = Column(DateTime,      nullabe=False, default=datetime.datetime.utcnow)

def as_dict(self):
    result = {getattr(self, col.name) for col in self.__table__.columns}
    return result

def add_data(data):
    db.session.add(data)
    db.session.commit()

def list():
    return SensorData.query.all()