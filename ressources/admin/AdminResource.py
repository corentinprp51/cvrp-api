from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.Users import Users, user_schema, users_schema
from database import db
from errors.error import AdminError, NotFoundError

class AdminResource(Resource):
    @jwt_required()
    def post(self):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        if user.isadmin:
            # Set username to admin too
            userId = request.json.get("userId", None)
            userToSetAdmin = Users.query.filter_by(id=userId).first() # Get user
            if userToSetAdmin != None:
                if not userToSetAdmin.isadmin:
                    userToSetAdmin.isadmin = True
                    db.session.commit()
                    return jsonify(user=user_schema.dump(userToSetAdmin))
                raise AdminError('User already admin')
            raise NotFoundError('User not found')
        raise AdminError("User not allowed to do this")

    @jwt_required()
    def get(self):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        if user.isadmin:
            return jsonify(admins=users_schema.dump(Users.query.filter_by(isadmin=True).all()))
        raise AdminError("User not allowed to do this")

