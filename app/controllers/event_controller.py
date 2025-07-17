from flask import Blueprint, jsonify, request
from app.services.recommendation_service import RecommendationService
from app.models.event import Event
from app.extensions import db


event_blueprint = Blueprint('event', __name__)
recommendation_service = RecommendationService()

@event_blueprint.route('/recommendation_events', methods=['GET'])

def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location,
        'popularity_score': e.popularity_score
    } for e in events])

@event_blueprint.route('/recommendation_events/<int:event_id>', methods=['GET'])

def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'category': event.category,
        'location': event.location,
        'popularity_score': event.popularity_score
    })

@event_blueprint.route('/recommendation_events', methods=['POST'])

def create_event():
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        location=data['location'],
        popularity_score=data.get('popularity_score', 0.0)
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created', 'id': event.id}), 201

@event_blueprint.route('/recommendation_events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(event, key, value)
    db.session.commit()
    return jsonify({'message': 'Event updated'})

@event_blueprint.route('/recommendation_events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'})

@event_blueprint.route('/recommendation_events/recommend/<int:event_id>', methods=['GET'])
def get_recommendations(event_id):
    recommendations = recommendation_service.get_similar_by_description(event_id)
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location
    } for e in recommendations])

@event_blueprint.route('/recommendation_events/recommend', methods=['GET'])

def get_hybrid_recommendations():
    category = request.args.get('category')
    location = request.args.get('location')
    recommendations = recommendation_service.get_ai_recommendations(
        category=category,
        location=location
    )
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location
    } for e in recommendations])
@event_blueprint.route('/recommendation_events/filter/category/<string:category>', methods=['GET'])
def filter_events_by_category(category):
    """Filter events by category"""
    events = recommendation_service.filter_by_category(category)
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location,
        'popularity_score': e.popularity_score
    } for e in events])

@event_blueprint.route('/recommendation_events/filter/location/<string:location>', methods=['GET'])
def filter_events_by_location(location):
    """Filter events by location"""
    events = recommendation_service.filter_by_location(location)
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location,
        'popularity_score': e.popularity_score
    } for e in events])

@event_blueprint.route('/recommendation_events/search', methods=['GET'])
def search_events_by_title():
    """Search events by title keyword"""
    keyword = request.args.get('q', '')
    events = recommendation_service.search_by_title(keyword)
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location,
        'popularity_score': e.popularity_score
    } for e in events])

@event_blueprint.route('/recommendation_events/filter', methods=['GET'])
def filter_events():
    """Filter events by both category and location"""
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    
    # Use the combined filter if both parameters exist
    if category and location:
        events = [e for e in recommendation_service.get_all() 
                 if category.lower() in e.category.lower() 
                 and location.lower() in e.location.lower()]
    elif category:
        events = recommendation_service.filter_by_category(category)
    elif location:
        events = recommendation_service.filter_by_location(location)
    else:
        events = recommendation_service.get_all()
    
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location,
        'popularity_score': e.popularity_score
    } for e in events])

@event_blueprint.route('/recommendation_events/recommend/basic', methods=['GET'])
def get_basic_recommendations():
    """Get basic recommendations based on category and location"""
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    recommendations = recommendation_service.recommend(category, location)
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category': e.category,
        'location': e.location
    } for e in recommendations])


@event_blueprint.route('/health')
def health_check():
    return jsonify({"status": "UP"}), 200