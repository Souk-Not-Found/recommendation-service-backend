from flask_restx import Resource
from flask import request
from app.schemas.event_schema import event_model, preferences_model
from app.services.recommendation_service import RecommendationService
from app.swagger import recommendation_ns

recommendation_service = RecommendationService()

@recommendation_ns.route('')
class RecommendationList(Resource):
    @recommendation_ns.expect(preferences_model)
    @recommendation_ns.marshal_list_with(event_model)
    def post(self):
        """Get recommended events based on category and location"""
        data = request.json
        return recommendation_service.recommend(data['category'], data['location'])

    @recommendation_ns.marshal_list_with(event_model)
    def get(self):
        """Get all events"""
        return recommendation_service.get_all()

@recommendation_ns.route('/<int:event_id>')
class RecommendationDetail(Resource):
    @recommendation_ns.marshal_with(event_model)
    def get(self, event_id):
        """Get event by ID"""
        return recommendation_service.get_by_id(event_id)

    @recommendation_ns.expect(event_model)
    @recommendation_ns.marshal_with(event_model)
    def put(self, event_id):
        """Update event"""
        data = request.json
        return recommendation_service.update(event_id, data)

    def delete(self, event_id):
        """Delete event"""
        recommendation_service.delete(event_id)
        return {'message': 'Deleted'}, 204

@recommendation_ns.route('/create')
class RecommendationCreate(Resource):
    @recommendation_ns.expect(event_model)
    @recommendation_ns.marshal_with(event_model)
    def post(self):
        """Create a new event"""
        data = request.json
        return recommendation_service.create(data)


@recommendation_ns.route('/filter/category/<string:category>')
class FilterByCategory(Resource):
    @recommendation_ns.marshal_list_with(event_model)
    def get(self, category):
        """Filter events by category"""
        return recommendation_service.filter_by_category(category)

@recommendation_ns.route('/filter/location/<string:location>')
class FilterByLocation(Resource):
    @recommendation_ns.marshal_list_with(event_model)
    def get(self, location):
        """Filter events by location"""
        return recommendation_service.filter_by_location(location)

@recommendation_ns.route('/search/<string:keyword>')
class SearchByTitle(Resource):
    @recommendation_ns.marshal_list_with(event_model)
    def get(self, keyword):
        """Search events by title"""
        return recommendation_service.search_by_title(keyword)
@recommendation_ns.route('/ai-recommendations')
class AIRecommendations(Resource):
    @recommendation_ns.expect(preferences_model)
    @recommendation_ns.marshal_list_with(event_model)
    def post(self):
        """Get AI-powered recommendations based on category and location"""
        data = request.json
        return recommendation_service.get_ai_recommendations(
            category=data.get('category'),
            location=data.get('location')
        )

@recommendation_ns.route('/similar/<int:event_id>')
class SimilarRecommendations(Resource):
    @recommendation_ns.marshal_list_with(event_model)
    def get(self, event_id):
        """Get similar events based on NLP description analysis"""
        return recommendation_service.get_similar_by_description(event_id)
        

