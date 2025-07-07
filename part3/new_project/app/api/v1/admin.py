#!/usr/bin/python3
"""
Admin endpoints for managing users and amenities
Only accessible to admin users (RBAC)
*Exigé par l'énoncé - Tâche 5 : Implement Administrator Access Endpoints
"""

from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from models.user import User
from models.amenity import Amenity
from facade import HBnBFacade

api = Namespace('admin', description='Admin operations')
facade = HBnBFacade()


# Exigé par l'énoncé - Endpoint POST /users/ (Admin only)
@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        """
        Create a new user (admin only)
        *Exigé par l'énoncé - Tâche 5
        """

        # Vérifie les droits admin via le JWT
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Récupère les données envoyées en JSON
        user_data = request.get_json()
        email = user_data.get('email')

        # Vérifie que l'email est présent
        if not email:
            return {'error': 'Email is required'}, 400

        # Vérifie si l'email est déjà utilisé
        existing_user = facade.get_user_by_email(email)
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Crée un nouvel utilisateur via la façade
        new_user = facade.create_user(user_data)

        # Retourne les informations du nouvel utilisateur
        return new_user.to_dict(), 201
