from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from database import db
from models.Users import Users, users_schema

class UserRegisterResource(Resource):
    def post(self):
        username = request.json.get("username", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        firstname = request.json.get("firstname", None)
        lastname = request.json.get("lastname", None)
        hash_password = generate_password_hash(password)
        user = Users()
        user.email = email
        user.password = hash_password
        user.username = username
        user.lastname = lastname
        user.firstname = firstname
        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=username)
            response = jsonify(access_token=access_token)
            response.status_code = 201 # or 400 or whatever
            return response
        except Exception as err:
            response = jsonify(error="Parameters required are not valid")
            response.status_code = 404 # or 400 or whatever
            return response