from app.models import db

class SQLAlchemyRepository:
    """CRUD générique basé sur SQLAlchemy."""
    def __init__(self, model):
        self.model = model

    # CREATE
    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    # READ
    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def get_by_attribute(self, attr, val):
        return self.model.query.filter(getattr(self.model, attr) == val).first()

    # UPDATE
    def update(self, obj_id, data: dict):
        obj = self.get(obj_id)
        if not obj:
            raise KeyError(f'{self.model.__name__} not found')
        for k, v in data.items():
            setattr(obj, k, v)
        db.session.commit()
        return obj

    # DELETE
    def delete(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            raise KeyError(f'{self.model.__name__} not found')
        db.session.delete(obj)
        db.session.commit()
