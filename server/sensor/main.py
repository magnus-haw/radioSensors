from sensor import Sensor

if __name__ == '__main__':
    sensor = Sensor()
    while True:
        sensor.loop()