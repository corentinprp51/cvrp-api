from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.Users import Users
from models.Model import models_schema, Model
from database import db
from sqlalchemy import desc

class ModelListResource(Resource):
    @jwt_required()
    def get(self):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        result = db.session.execute(db.select(Model).where(Model.user_id==user.id).order_by(desc(Model.creation_date), desc(Model.last_edit)))
        liste = result.scalars().all()
        return jsonify(models=models_schema.dump(liste))

