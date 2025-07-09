from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.services.repositories.user_repository import UserRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # USER
    def create_user(self, user_data, plain_password):
        user = User(**user_data)
        user.hash_password(plain_password)
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data):
        user = self.user_repo.get_by_attribute('id', place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data')
        del place_data['owner_id']
        place_data['owner'] = user

        amenities = place_data.pop('amenities', None)
        if amenities:
            resolved_amenities = []
            for a in amenities:
                amenity = self.get_amenity(a['id'])
                if not amenity:
                    raise KeyError('Invalid amenity ID')
                resolved_amenities.append(amenity)

        place = Place(**place_data)
        self.place_repo.add(place)

        user.places.append(place)
        if amenities:
            for amenity in resolved_amenities:
                place.amenities.append(amenity)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    # REVIEW
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid user ID')
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid place ID')

        del review_data['user_id']
        del review_data['place_id']
        review_data['user'] = user
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)

        user.reviews.append(review)
        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def get_reviews_by_place_and_user(self, place_id, user_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")
        return [review for review in place.reviews if review.user.id == user_id]

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        user.reviews.remove(review)
        place.reviews.remove(review)
        self.review_repo.delete(review_id)
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.services.repositories.user_repository import UserRepository
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # USER
    def create_user(self, user_data, plain_password):
        user = User(**user_data)
        user.hash_password(plain_password)
        self.user_repo.add(user)
        return user

    def get_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data):
        user = self.user_repo.get_by_attribute('id', place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data')
        del place_data['owner_id']
        place_data['owner'] = user

        amenities = place_data.pop('amenities', None)
        if amenities:
            resolved_amenities = []
            for a in amenities:
                amenity = self.get_amenity(a['id'])
                if not amenity:
                    raise KeyError('Invalid amenity ID')
                resolved_amenities.append(amenity)

        place = Place(**place_data)
        self.place_repo.add(place)

        user.places.append(place)
        if amenities:
            for amenity in resolved_amenities:
                place.amenities.append(amenity)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)

    # REVIEW
    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid user ID')
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid place ID')

        del review_data['user_id']
        del review_data['place_id']
        review_data['user'] = user
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repo.add(review)

        user.reviews.append(review)
        place.reviews.append(review)

        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def get_reviews_by_place_and_user(self, place_id, user_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise KeyError("Place not found")
        return [review for review in place.reviews if review.user.id == user_id]

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        user = self.user_repo.get(review.user.id)
        place = self.place_repo.get(review.place.id)

        user.reviews.remove(review)
        place.reviews.remove(review)
        self.review_repo.delete(review_id)
