from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField
from mongoengine.fields import EmailField, IntField, ReferenceField, DateTimeField, ListField,ObjectIdField


class Registration(Document):
    email = EmailField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)  
    role = StringField(choices=['User', 'Lawyer'], required=True)
    phone_number = StringField(required=True)
    address = StringField(required=True)
    gender = StringField(choices=['Male', 'Female'], required=True)
    dob = DateTimeField(required=True)
    state = StringField(required=True)
    country = StringField(required=True)
    pin_code = IntField(required=True)
    
    occupation = StringField()
    
    field_of_expertise = StringField()
    number_of_cases_won = IntField()
    years_of_experience = IntField()


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
