from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.Users import Users, users_schema

class UserLoginResource(Resource):
    def post(self):
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if username == None or password == None:
            response = jsonify({"error": "Username and password are required"})
            response.status_code = 404 # or 400 or whatever
            return response
        try:            
            user = Users.query.filter(Users.username == username).one()
            if not check_password_hash(user.password, password):
                response = jsonify({"error": "Bad username or password"})
                response.status_code = 404 # or 400 or whatever
                return response

            #Test with additional data in JWT token
            additional_claims = {"aud": "some_audience", "foo": "bar"}
            access_token = create_access_token(identity=username, additional_claims=additional_claims)
            return jsonify(access_token=access_token)
        except Exception as e:
                response = jsonify({"error": "Bad username or password"})
                response.status_code = 404 # or 400 or whatever
                return response