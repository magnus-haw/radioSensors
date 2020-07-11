from sensor import Experiment
import requests

FLASK_URL = 'http://10.0.0.14/temperature'

if __name__ == '__main__':
    experiment = Experiment("test")
    experiment.listen()
    # for cache in sensor.loop(): 
    #     print(cache)
    #     if (cache):
    #         requests.post(FLASK_URL, json=cache)