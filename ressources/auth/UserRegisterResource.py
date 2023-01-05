from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash
from database import db
from models.Users import Users, user_schema
from errors.error import AuthError

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
            additional_claims = {"userId": user.id, "email": email, "isAdmin": False, "firstname": firstname, "lastname": lastname, "username": username}
            access_token = create_access_token(identity=username, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=username)
            response = jsonify(access_token=access_token, refresh_token=refresh_token, user=user_schema.dump(user))
            response.status_code = 201 # or 400 or whatever
            return response
        except Exception as err:
            print(err)
            raise AuthError('Informations needed are invalid')