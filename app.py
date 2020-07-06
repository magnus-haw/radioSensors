#app.py

from flask import Flask
from models import *
from service import *
from flask import request

app = Flask(__name__) # what does create an app
# app.debug = True

@app.route("/", methods=["GET","POST"])
def create_todo():
    return ToDoService().create(request.get_json())

if __name__ == "__main__":
    Schema() # is there anything I need to do to specify that this is a class?
    app.run(debug=True)