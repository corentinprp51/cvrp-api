from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.Users import Users, user_schema
from database import db
from errors.error import AdminError, NotFoundError, AuthError
from werkzeug.security import generate_password_hash

class UserResource(Resource):
    @jwt_required()
    def get(self, userId=None):
        username = get_jwt_identity()
        user = Users.query.filter_by(username=username).first()
        return jsonify(user_schema.dump(user))
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
    @jwt_required()
    def put(self, userId):
        claims = get_jwt()
        if (userId == claims["userId"]):
            #Edit des champs firstname, lastname, password
            user = Users.query.filter_by(id=userId).first()
            if (user):
                firstname = request.json.get("firstname", None)
                lastname = request.json.get("lastname", None)
                password = request.json.get("password", "")
                confirm_password = request.json.get("confirm_password", "")
                if (password != "" and confirm_password != ""):
                    if (password == confirm_password):
                        hash_password = generate_password_hash(password)
                        user.password = hash_password
                    else: 
                        raise AuthError('The two passwords must be the same')
                user.firstname = firstname
                user.lastname = lastname
                db.session.commit()
                return jsonify(firstname=firstname, lastname=lastname)
            else: 
                raise NotFoundError('User not found')
        else:
            #Check if the user is admin
            userToEdit = Users.query.filter_by(id=userId).first()
            userAdmin = Users.query.filter_by(id=claims["userId"]).first()
            if(userAdmin and user and userAdmin.isadmin):
                username = request.json.get("username", ""),
                email = request.json.get("email", ""),
                firstname = request.json.get("firstname", "")
                lastname = request.json.get("lastname", "")
                password = request.json.get("password", "")
                confirm_password = request.json.get("confirm_password", "")
                if (password != "" and confirm_password != ""):
                    if (password == confirm_password):
                        hash_password = generate_password_hash(password)
                        user.password = hash_password
                    else: 
                        raise AuthError('The two passwords must be the same')
                if (username != ""):
                    user.username = username
                else: 
                    raise AuthError("The username musn't be null")
                if (email != ""):
                    user.email = email
                else:
                    raise AuthError("The email musn't be null")
                user.firstname = firstname
                user.lastname = lastname
                try:
                    db.session.commit()
                    return jsonify(user_schema.dump(user))
                except Exception:
                    raise AuthError("Username or email field are not unique")
            else:
                raise AuthError('User not admin or user to edit not exist')



