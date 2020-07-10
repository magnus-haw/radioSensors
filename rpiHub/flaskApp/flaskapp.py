from flask import Flask
from flask import render_template

app = Flask(__name__)



@app.route('/<name>')
def sensor(name=None,temp=None):
    temp = 75 ###acquire temperature measurement here
    return render_template('sensor.html', name=name, temp=temp)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == "__main__":        # on running python app.py
    app.run(host= '0.0.0.0', debug=True)                    # run the flask app
