from frontend import db
from frontend.models import Sensor, Point
from .radio import RadioBonnet

radio = RadioBonnet()
CACHE_LEVEL = 5

def init_radio(experiment):
    cache = []

    for data in radio.listen():
        sensor = Sensor.filter_by(name=data['name']).first()
        if not sensor:
            sensor = Sensor(name=data['name'], unit=data['unit'])
            db.session.add(sensor)
        point = Point(
            data=data['value'],
            sensor=sensor,
            experiment=experiment
        )
        db.session.add(point)
        db.session.commit()