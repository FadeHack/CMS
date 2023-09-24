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
    case_name = StringField(required=True)
    case_type = StringField(required=True)
    case_description = StringField(required=True)
    aadhar_number = IntField(required=True)
    role = StringField(choices=['User', 'Lawyer'], required=True)
    

