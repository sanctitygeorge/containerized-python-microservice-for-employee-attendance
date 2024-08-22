# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize migration support
    jwt.init_app(app)  # Initialize JWT

    # Import models so that they are registered with SQLAlchemy
    from app.models import User, Attendance

    # Register blueprints
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
