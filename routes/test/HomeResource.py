from flask import jsonify
from flask_restful import Resource
from models.Users import Users, users_schema

class HomeResource(Resource):
    def get(self):
        users = Users.query.all()
        return jsonify(users=users_schema.dump(users)) 