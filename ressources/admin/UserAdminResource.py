from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.Users import Users, user_schema
from database import db
from errors.error import AdminError, NotFoundError, AuthError
from werkzeug.security import generate_password_hash

class UserAdminResource(Resource):
    @jwt_required()
    def get(self, userId):
        username = get_jwt_identity()
        user = Users.query.filter_by(username=username).first()
        if (user.isadmin):
            userToGet = Users.query.filter_by(id=userId).first()
            return jsonify(user_schema.dump(userToGet))
        else:
            raise AdminError('User is not admin')