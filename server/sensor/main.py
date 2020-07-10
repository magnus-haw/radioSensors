from sensor import Sensor
import requests

FLASK_URL = '10.0.0.14/temperature'

if __name__ == '__main__':
    sensor = Sensor()
    for cache in sensor.loop(): 
        if (cache):
            requests.post(FLASK_URL, json=cache)