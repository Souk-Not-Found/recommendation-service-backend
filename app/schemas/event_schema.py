from flask_restx import fields
from app.swagger import api

event_model = api.model('Event', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'category': fields.String,
    'location': fields.String,
    'popularity_score': fields.Float
})

preferences_model = api.model('Preferences', {
    'category': fields.String,
    'location': fields.String
})
