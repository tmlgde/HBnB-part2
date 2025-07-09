# app/persistence/repository.py

from app import db

class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()

    def update(self):
        db.session.commit()
