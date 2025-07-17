import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql://postgres:anas2000@localhost/recommendation_db"  # fallback
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Eureka configuration
    EUREKA_SERVER_URL = os.getenv("EUREKA_SERVER_URL", "http://localhost:8761/eureka")
    APP_NAME = os.getenv("APP_NAME", "event-recommendation-service")
    INSTANCE_PORT = int(os.getenv("SERVER_PORT", 5000))
    INSTANCE_HOST = os.getenv("INSTANCE_HOST", "localhost")
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200")