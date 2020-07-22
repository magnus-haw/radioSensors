from frontend import app
import threading

if __name__ == "__main__":
    # sensor_thread = threading.Thread(target=run_sensor)
    # sensor_thread.start()

    app.run(host='0.0.0.0', debug=True)