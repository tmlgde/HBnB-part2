from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager  # ← AJOUT

from app.config import DevelopmentConfig
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)  # ← AJOUT

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth') 

    return app
