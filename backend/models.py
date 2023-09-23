from mongoengine import Document, StringField, ListField, ReferenceField
from mongoengine.fields import ObjectIdField


class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
        }


class Case(Document):
    cnr = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField(required=True)
    status = StringField(required=True)
    lawyer_id = ObjectIdField(required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "cnr": self.cnr,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "lawyer_id": str(self.lawyer_id),
        }


class Lawyer(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    bar_number = StringField(required=True, unique=True)
    specialization = StringField(required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "bar_number": self.bar_number,
            "specialization": self.specialization,
        }


class Admin(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
        }
