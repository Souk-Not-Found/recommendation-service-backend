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
    """Register this service with Eureka server"""
    try:
        eureka_client.init(
            eureka_server=app.config['EUREKA_SERVER_URL'],
            app_name="event-recommendation-service",  # Must match gateway config
            instance_port=app.config['INSTANCE_PORT'],
            instance_host=app.config['INSTANCE_HOST'],
            renewal_interval_in_secs=10,
            duration_in_secs=30,
            metadata={
                "management.port": str(app.config['INSTANCE_PORT']),
                "healthCheckUrl": f"http://{app.config['INSTANCE_HOST']}:{app.config['INSTANCE_PORT']}/health",
                "statusPageUrl": f"http://{app.config['INSTANCE_HOST']}:{app.config['INSTANCE_PORT']}/health"
            }
        )
        app.logger.info(f"✅ Registered as event-recommendation-service at {app.config['INSTANCE_HOST']}:{app.config['INSTANCE_PORT']}")
    except Exception as e:
        app.logger.error(f"❌ Eureka registration failed: {str(e)}")
        # Implement retry logic here if needed