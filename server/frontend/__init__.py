from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from . import models
db.create_all() 

from . import routes
from . import admin

# app.register_blueprint(auth.auth_bp)
# app.register_blueprint(admin.admin_bp)