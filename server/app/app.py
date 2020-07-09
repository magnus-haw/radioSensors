from flask import Flask
from flask import request
from models import Schema
from models import TemperatureModel
app = Flask(__name__)

@app.route("/")
def show_data():
    return TemperatureModel().get().split(' ')

@app.route("/", methods=["POST"])
def insert_data():
    print(request.get_json())
    return str(TemperatureModel().update(data=request.get_json()))

if __name__ == "__main__":
    Schema()
    app.run()
    