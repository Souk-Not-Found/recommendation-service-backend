from py_eureka_client import eureka_client


def init_eureka(app):
    try:
        eureka_client.init(
            eureka_server=app.config['EUREKA_SERVER_URL'],
            app_name=app.config['APP_NAME'],
            instance_port=app.config['INSTANCE_PORT'],
            instance_host="event-recommendation-service"  # Docker service name
        )
        app.logger.info("Successfully registered with Eureka")
    except Exception as e:
        app.logger.error(f"Failed to register with Eureka: {e}")