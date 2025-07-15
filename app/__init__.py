from flask import Flask
from .extensions import db
from .config import Config
import py_eureka_client.eureka_client as eureka_client

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Eureka client with proper configuration
    register_with_eureka(app)
    
    # Register blueprints
    from .controllers.event_controller import event_blueprint
    app.register_blueprint(event_blueprint)
    
    return app

def register_with_eureka(app):
    """Helper function to register with Eureka server"""
    try:
        eureka_client.init(
            eureka_server=app.config.get('EUREKA_SERVER_URL', "http://localhost:8761/eureka"),
            app_name=app.config.get('APP_NAME', "recommendation-service"),
            instance_port=app.config.get('INSTANCE_PORT', 5000),
            instance_host=app.config.get('INSTANCE_HOST', "localhost"),
            renewal_interval_in_secs=30,
            duration_in_secs=90,
            metadata={
                "management.port": str(app.config.get('INSTANCE_PORT', 5000)),
                "healthCheckUrl": f"http://{app.config.get('INSTANCE_HOST', 'localhost')}:{app.config.get('INSTANCE_PORT', 5000)}/health"
            }
        )
        app.logger.info("Successfully registered with Eureka")
    except Exception as e:
        app.logger.error(f"Failed to register with Eureka: {str(e)}")
        # Continue running even if Eureka registration fails