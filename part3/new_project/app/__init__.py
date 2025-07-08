#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.config import DevelopmentConfig
from app.models import db            # ← même instance partout

# extensions
bcrypt = Bcrypt()
jwt    = JWTManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # API v1
    api = Api(app, title='HBnB API', version='1.0')

    from app.api.v1.auth    import api as auth_ns
    from app.api.v1.admin   import api as admin_ns
    from app.api.v1.places  import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    api.add_namespace(auth_ns,   path='/api/v1/auth')
    api.add_namespace(admin_ns,  path='/api/v1/admin')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
