#!/usr/bin/python3
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # NEW
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(description='Rating (1-5)'),
    'place_id': fields.String(required=True),
    'user_id': fields.String
})

@api.route('/')
class ReviewList(Resource):
    # ----- POST omitted (inchangé) -----
    # ----- GET omitted (inchangé) -----
    pass


@api.route('/<review_id>')
class ReviewResource(Resource):
    # ----- GET omitted (inchangé) -----

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # -------- RBAC admin bypass --------
        claims   = get_jwt()                         # NEW
        is_admin = claims.get('is_admin', False)     # NEW
        if not is_admin and (not review.user or review.user.id != current_user_id):  # MOD
            return {'error': 'Unauthorized action'}, 403
        # -----------------------------------

        try:
            facade.update_review(review_id, api.payload)
            return {'message': 'Review updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # -------- RBAC admin bypass --------
        claims   = get_jwt()                         # NEW
        is_admin = claims.get('is_admin', False)     # NEW
        if not is_admin and (not review.user or review.user.id != current_user_id):  # MOD
            return {'error': 'Unauthorized action'}, 403
        # -----------------------------------

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
