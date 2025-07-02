#!/usr/bin/python3
from app import create_app
from app.services import facade

app = create_app()

with app.app_context():
    user_data = {
        "email": "admin@hbnb.com",
        "password": "admin123",
        "first_name": "Admin",
        "last_name": "User",
        "is_admin": True
    }

    user = facade.create_user(user_data)
    print(f"Utilisateur créé avec l'ID : {user.id}")
