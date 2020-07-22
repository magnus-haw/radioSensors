from frontend import app
from sensor import init_radio
import threading

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=init_radio)
    sensor_thread.start()

    app.run(host='0.0.0.0', debug=True)