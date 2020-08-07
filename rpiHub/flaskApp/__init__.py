from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

# Globally accessible libraries
db = SQLAlchemy()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
   
    ### Needed to enforce foreign keys in sqlite databases
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    # Initialize Plugins
    db.init_app(app)
    
    with app.app_context():
        from . import routes  # Import routes
        from . import admin
        db.create_all()       # Create sql tables

        # Register Blueprints
#        app.register_blueprint(auth.auth_bp)
#        app.register_blueprint(admin.admin_bp)

        return app
    

