#!/usr/bin/python3
"""
Authentication endpoints (login + bootstrap admin temporaire)
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# ---------- Models ----------
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# ---------- Routes ----------
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        creds = request.get_json()
        user  = facade.get_user_by_email(creds['email'])
        if not user or not user.verify_password(creds['password']):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity={'id': user.id, 'is_admin': user.is_admin}
        )
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {'message': f'Hello, user {current_user_id}'}, 200


# ---------- BOOTSTRAP ADMIN (temporaire) ----------
@api.route('/bootstrap_admin')
class BootstrapAdmin(Resource):
    """
    Create an initial admin account if it doesn't exist.
    Call **once**, then remove this route for production.
    """
    def post(self):
        if facade.get_user_by_email("admin@example.com"):
            return {"msg": "admin exists"}, 200

        admin = facade.create_user({
            "email": "admin@example.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "User",
            "is_admin": True
        })
        return admin.to_dict(), 201
