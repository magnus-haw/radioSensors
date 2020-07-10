#app.py

from flask import Flask
from models import *
from service import *
from flask import request,jsonify

app = Flask(__name__) # what does create an app
# app.debug = True

@app.route("/todo", methods=["POST"])
def create_todo():
    return jsonify(ToDoService().create(request.get_json()))

@app.route("/todo", methods=["GET"])
def list_todo():
    return jsonify(ToDoService().list())

if __name__ == "__main__":
    Schema() # is there anything I need to do to specify that this is a class?
    app.run(host= '0.0.0.0', debug=True)
