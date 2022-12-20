from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.Users import Users, users_schema
from sqlalchemy.orm import joinedload
from errors.error import AdminError

class ListUsersResource(Resource):
    @jwt_required()
    def get(self):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        if user.isadmin:
            return jsonify(users=users_schema.dump(Users.query.options(joinedload('models')).all()))
        raise AdminError('User not allowed to access it')

