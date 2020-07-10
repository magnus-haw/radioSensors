from sensor import Sensor

if __name__ == '__main__':
    sensor = Sensor()
    for cache in sensor.loop(): print(cache)