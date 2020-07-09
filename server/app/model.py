import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from flask_restful import reqparse
from app import db

class SensorData(db.Model):
    id          = Column(Integer,       nullable=False, primary_key=True)
    data        = Column(Float,         nullable=False)
    timestamp   = Column(DateTime,      nullable=False, default=datetime.datetime.utcnow)

    def as_dict(self):
        result = {getattr(self, col.name) for col in self.__table__.columns}
        return result

def add_data(data):
    parser = reqparse.RequestParser()
    parser.add_argument('data', type=float, required=True)

    data = parser.parse_args()

    db.session.add(SensorData(**data))
    db.session.commit()

def list():
    return SensorData.query.all()

db.create_all()
db.session.commit()
print('created')