from frontend.models import Sensor, Point
from radio import RadioBonnet

radio = RadioBonnet()
CACHE_LEVEL = 5

def init_radio():
    cache = []

    for data in radio.listen():
        print(data)
