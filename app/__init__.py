from flask import Flask
from app.extensions import db
from flask_cors import CORS
from app.swagger import api

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    CORS(app)
    db.init_app(app)

    # Import routes after app creation to avoid circular imports
    from app.routes.recommendation_routes import recommendation_ns
    api.add_namespace(recommendation_ns)

    # Initialize API with app
    api.init_app(app)

    return app