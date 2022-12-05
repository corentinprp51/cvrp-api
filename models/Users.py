from database import db, ma
from models.Model import Model

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=True)
    lastname = db.Column(db.String, nullable=True)
    models = db.relationship('Model', backref='user')

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "firstname", "lastname", "models")
        model = Users

user_schema = UserSchema()
users_schema = UserSchema(many=True)