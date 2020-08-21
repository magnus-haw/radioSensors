import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime
from . import db

# Defining a schema for each category
class Point(db.Model):
    id              = db.Column(db.Integer,       nullable=False,    primary_key=True)
    data            = db.Column(db.Float,         nullable=False)
    time            = db.Column(db.DateTime,      nullable=False,  default=datetime.datetime.utcnow)

    def as_dict(self):
        result = {getattr(self, col.name) for col in self.__table__.columns}
        return result

    def __repr__(self):
        return '<Point id=%i, data=%f, time=%s>' \
    %(self.id, self.data, self.time)
