from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import threading

# Globally accessible libraries
db = SQLAlchemy()
sess = Session()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    # Initialize Plugins
    db.init_app(app)
    sess.init_app(app)
    
    with app.app_context():
        from .radio import RadioBonnet

        radio = RadioBonnet()
        session['radio'] = radio
        sensor_thread = threading.Thread(target=radio.listen)
        sensor_thread.start()

        from . import routes  # Import routes
        from . import admin
        db.create_all()       # Create sql tables

        
        
        # Register Blueprints
#        app.register_blueprint(auth.auth_bp)
#        app.register_blueprint(admin.admin_bp)

        return app