import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://postgres:anas2000@localhost/recommendation_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
