from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.Users import Users
from database import db
from errors.error import AdminError, NotFoundError

class UserResource(Resource):
    @jwt_required()
    def delete(self, userId):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        if user.isadmin:
            userToDelete = Users.query.filter_by(id=userId).first() # Get user
            if userToDelete != None:
                db.session.delete(userToDelete)
                db.session.commit()
                return jsonify(userId=userId)
            raise NotFoundError("User not found")
        raise AdminError("User not allowed to do this")

