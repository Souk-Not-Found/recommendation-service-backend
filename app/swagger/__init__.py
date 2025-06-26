from flask_restx import Api, Namespace

api = Api(
    title='Recommendation API',
    version='1.0',
    description='API for event recommendations',
)

recommendation_ns = Namespace('recommendations', description='Event recommendations operations')