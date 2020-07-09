import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resource={r"/*": {"origins": "*"}})
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['RADIO_SENSOR_DB'] # for production

api = Api(app)
db = SQLAlchemy(app)

import .endpoints

db.create_all()
db.session.commit()