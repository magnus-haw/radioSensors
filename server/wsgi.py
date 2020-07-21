from frontend import app
from sensor import run_sensor
import threading

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=run_sensor)
    sensor_thread.start()

    app.run(host='0.0.0.0', debug=True)