from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import threading

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
session = Session(app)

from . import models
db.create_all() 

from . import routes
from . import admin

from .radio import RadioBonnet
radio = RadioBonnet()
session['radio'] = radio
sensor_thread = threading.Thread(target=radio.listen)
sensor_thread.start()

# app.register_blueprint(auth.auth_bp)
# app.register_blueprint(admin.admin_bp)