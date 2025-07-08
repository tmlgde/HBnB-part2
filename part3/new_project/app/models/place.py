from app import db
from sqlalchemy.orm import validates
from .user import User
from .review import Review
from .amenity import Amenity
import uuid

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String, db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String, db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='places')

    reviews = db.relationship('Review', backref='place', cascade="all, delete-orphan")
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        if len(value) > 100:
            raise ValueError("Title must be 100 characters max.")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a positive number")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, float):
            raise ValueError("Latitude must be a float")
        if not -90 < value < 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, float):
            raise ValueError("Longitude must be a float")
        if not -180 < value < 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id
        }

    def to_dict_list(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict() if self.owner else None,
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews]
        }
