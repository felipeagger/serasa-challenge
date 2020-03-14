from dbconf.db import db, ma
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from flask_marshmallow import Marshmallow

class User(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, index = True)
    cpf = db.Column(db.String(255)) #11
    email = db.Column(db.String(255)) #150
    phone_number = db.Column(db.String(255)) #15
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())

    def __init__(self, name, cpf, email, phone_number):
        self.name = name
        self.cpf = cpf
        self.email = email
        self.phone_number = phone_number


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'cpf', 'email', 'phone_number', 'created_at', 'updated_at')


user_schema = UserSchema()
users_schema = UserSchema(many=True)        