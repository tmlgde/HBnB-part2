from app import db
from sqlalchemy.orm import validates
import re

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        if len(value) > 50:
            raise ValueError("First name too long")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        if len(value) > 50:
            raise ValueError("Last name too long")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value
