from flask_sqlalchemy import SQLAlchemy
import py_eureka_client.eureka_client as eureka_client

db = SQLAlchemy()
# No need to initialize Eureka here - we'll do it in app factory