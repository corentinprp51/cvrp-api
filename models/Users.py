from database import db, ma
from models.Model import ModelSchema

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String, nullable=True)
    lastname = db.Column(db.String, nullable=True)
    isadmin = db.Column(db.Boolean, default=False)
    models = db.relationship('Model', backref='user', cascade='all, delete', passive_deletes=True)

class UserSchema(ma.Schema):
    models = ma.Nested(ModelSchema, many=True)
    isAdmin = ma.Bool(attribute="isadmin")
    class Meta:
        fields = ("id", "username", "email", "firstname", "lastname", "models", "isAdmin")
        model = Users

user_schema = UserSchema()
users_schema = UserSchema(many=True)