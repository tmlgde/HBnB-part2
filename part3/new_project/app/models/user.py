from .basemodel import BaseModel
import re

class User(BaseModel):
    emails = set()

    def __init__(self, **kwargs):
        super().__init__()
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.email = kwargs.get('email')
        self.is_admin = kwargs.get('is_admin', False)
        self.places = []
        self.reviews = []
        self.password = None
        password = kwargs.get('password')
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """hash le mot de passe avant de le poser dans la base de donnees"""
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """verifie si le mot de passe fourni correspond au mot de passe hache"""
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)
    
    @property
    def first_name(self):
        return self.__first_name
    
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("First name must be a string")
        super().is_max_length('First name', value, 50)
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Last name must be a string")
        super().is_max_length('Last name', value, 50)
        self.__last_name = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        if value in User.emails:
            raise ValueError("Email already exists")
        if hasattr(self, "_User__email"):
            User.emails.discard(self.__email)
        self.__email = value
        User.emails.add(value)

    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise TypeError("Is Admin must be a boolean")
        self.__is_admin = value

    def add_place(self, place):
        """Add an amenity to the place."""
        self.places.append(place)

    def add_review(self, review):
        """Add an amenity to the place."""
        self.reviews.append(review)

    def delete_review(self, review):
        """Add an amenity to the place."""
        self.reviews.remove(review)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
