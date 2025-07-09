from app.extensions import db
from sqlalchemy.orm import validates
from .basemodel import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters max.")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
