from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade

authorizations = {
        'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Enter 'Bearer' followed by your JWT token"
    }
}
api = Namespace('users', description='User operations', authorizations=authorizations, security='Bearer Auth')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409

        try:
            plain_password = user_data.get('password') # 🔁 pas besoin de pop ici
            new_user = facade.create_user(user_data, plain_password)  # 👈 on passe les deux
            user_dict = new_user.to_dict()
            user_dict.pop('password', None)
            return user_dict, 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        user_dict = user.to_dict()
        user_dict.pop('password', None)
        return user_dict, 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def put(self, user_id):

        current_user_id = get_jwt_identity()

        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not claims.get("is_admin") and current_user_id != user_id:
            return {"error": "Unauthorized action"}, 403


        user_data = api.payload
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'Vous ne pouvez pas modifier votre adresse e-mail ou votre mot de passe'}, 400


        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        try:
            facade.update_user(user_id, user_data)
            return user.to_dict(), 200

        except Exception as e:
            return {'error': str(e)}, 400
