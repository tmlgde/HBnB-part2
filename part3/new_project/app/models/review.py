from app.extensions import db
from sqlalchemy.orm import validates
from .basemodel import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    @validates('text')
    def validate_text(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Text must be a string")
        if not 10 <= len(value) <= 500:
            raise ValueError("Text must be between 10 and 500 characters")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        }
