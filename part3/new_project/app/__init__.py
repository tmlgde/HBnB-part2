#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from app.extensions import db, bcrypt, jwt
from app.config import DevelopmentConfig
from app.models import db            # ← même instance partout

<<<<<<< HEAD
# extensions
bcrypt = Bcrypt()
jwt    = JWTManager()
=======

>>>>>>> main

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
<<<<<<< HEAD
    bcrypt.init_app(app)
    jwt.init_app(app)
=======
    jwt.init_app(app
            )
    from app.models import user
    with app.app_context():
        db.create_all()
>>>>>>> main

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
