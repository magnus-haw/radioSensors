from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import threading

# Globally accessible libraries
db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    # Initialize Plugins
    db.init_app(app)
    
    with app.app_context():
        from . import routes  # Import routes
        from . import admin
        db.create_all()       # Create sql tables

        from .radio import RadioBonnet
        radio = RadioBonnet()
        session['radio'] = radio
        sensor_thread = threading.Thread(target=radio.listen)
        sensor_thread.start()

        # Register Blueprints
#        app.register_blueprint(auth.auth_bp)
#        app.register_blueprint(admin.admin_bp)

        return app