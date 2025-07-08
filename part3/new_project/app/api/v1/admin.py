from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from app.services import facade

api = Namespace('admin', description='Admin operations')

user_in = api.model('UserIn', {
    'email': fields.String(required=True),
    'first_name': fields.String,
    'last_name': fields.String,
    'password': fields.String,
    'is_admin': fields.Boolean
})

# -- CREATE USER --
@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_in)
    @jwt_required()
    def post(self):
        if not get_jwt().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        try:
            user = facade.create_user(request.get_json())
            return user.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400

# -- UPDATE USER --
@api.route('/users/<string:user_id>')
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        if not get_jwt().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        try:
            user = facade.update_user(user_id, request.get_json())
            return user.to_dict(), 200
        except (KeyError, ValueError) as e:
            return {'error': str(e)}, 400