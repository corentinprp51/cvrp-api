from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.Users import Users
from models.Model import models_schema

class ModelListResource(Resource):
    @jwt_required()
    def get(self):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        return jsonify(models=models_schema.dump(user.models))

