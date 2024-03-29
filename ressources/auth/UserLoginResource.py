from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
from models.Users import Users, user_schema
from errors.error import AuthError

class UserLoginResource(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if username == None or password == None:
            raise AuthError('Invalid username or password')
        try:            
            user = Users.query.filter(Users.username == username).one()
            if not check_password_hash(user.password, password):
                raise AuthError('Invalid username or password')

            #Test with additional data in JWT token
            additional_claims = {"userId": user.id, "email": user.email, "isAdmin": user.isadmin, "firstname": user.firstname, "lastname": user.lastname, "username": username}
            access_token = create_access_token(identity=username, additional_claims=additional_claims)
            refresh_token = create_refresh_token(identity=username)
            return jsonify(access_token=access_token, refresh_token=refresh_token, user=user_schema.dump(user))
        except Exception:
                raise AuthError('Invalid username or password')