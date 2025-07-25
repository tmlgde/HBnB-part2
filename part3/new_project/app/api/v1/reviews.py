from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=False, description='ID of the user (from JWT)')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload
        place = facade.get_place(review_data['place_id'])

        if 'rating' not in review_data:
            review_data['rating'] = 5

        if not place:
            return {'error': 'Place not found'}, 400

        user = facade.get_user(current_user_id)
        if not user:
            return {'error': 'User not found'}, 400

        if place.owner.id == user.id:
            return {'error': 'User cannot review their own place'}, 400

        existing_reviews = facade.get_reviews_by_place_and_user(place.id, current_user_id)
        if existing_reviews:
            return {'error': 'You already have review this place'}, 400

        try:
            review_data['user_id'] = current_user_id
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    @api.doc(security='Bearer Auth')
    @jwt_required()
    def get(self):
        """Retrieve a list of all reviews"""
        return [review.to_dict() for review in facade.get_all_reviews()], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if not review.user or review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        review_data = api.payload
        try:
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if not review.user or review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
