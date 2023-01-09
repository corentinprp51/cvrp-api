from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ressources.models.ModelCVRPApi import ModelCVRPApi
from models.Users import Users
from models.Model import Model, model_schema
from database import db
import uuid
import os
from errors.error import NotAllowedError, NotFoundError
from utils.mail import MailTemplate
import datetime

class ModelResource(Resource):
    @jwt_required()
    def post(self, modelId=None):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        model = ModelCVRPApi()
        model.readFromData(request.json['data'])
        model.initModel(request.json['parameters']['vehicle_max_capacity'])
        model.optimizeModel(request.json['parameters'])
        needEmail = request.json.get('needEmail', False)
        id = str(uuid.uuid4())
        model.modelGurobi.write(id + '.sol')
        # Store the model
        # Assign the model to the current user
        modelDB = Model()
        modelDB.name = request.json.get("name", None)
        modelDB.parameters= request.json.get("parameters", None)
        modelDB.data_parameters= request.json.get("data", None)
        modelDB.solution= model.getRoutesFromSolution()
        modelDB.solution_path_file= ''
        modelDB.user = user
        with open(id + '.sol') as f:
            modelDB.file_solution_text = f.read()
            f.close()
        os.remove(id + '.sol')
        print('USER MODELS:', user.models)
        db.session.add(modelDB)
        db.session.commit()
        print(model.getRoutesFromSolution())
        if(needEmail):
            mailTemplate = MailTemplate(user.email, "CVRP - New Model " + modelDB.name + " Execution", "Execution ended!")
            mailTemplate.sendMail()
        return jsonify(model=model_schema.dump(modelDB))

    @jwt_required()
    def put(self, modelId):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        modelDB = Model.query.filter_by(id=modelId).first() # Get model
        parameters = request.json.get('parameters', None)
        name = request.json.get('name', modelDB.name)
        needEmail = request.json.get('needEmail', False)
        if parameters is None:
            parameters = modelDB.parameters
        if (user != None and (user.username == current_username or user.isadmin)):
            model = ModelCVRPApi()
            model.readFromData(modelDB.data_parameters)
            model.initModel(parameters['vehicle_max_capacity'])
            model.modelGurobi.update()

            #Create file with solution text
            with open(str(modelDB.id) + '.sol', 'w') as f:
                f.write(modelDB.file_solution_text)

            model.modelGurobi.read(str(modelDB.id) + '.sol')
            model.optimizeModel(parameters)
            model.modelGurobi.write(str(modelDB.id) + '.sol')
            with open(str(modelDB.id) + '.sol') as f:
                modelDB.file_solution_text = f.read()
                f.close()
            os.remove(str(modelDB.id) + '.sol')
            modelDB.solution = model.getRoutesFromSolution()
            modelDB.parameters = parameters
            modelDB.name = name
            modelDB.last_edit = datetime.datetime.now()
            db.session.commit()
            print(model.getRoutesFromSolution())
            if(needEmail):
                mailTemplate = MailTemplate(user.email, f"CVRP - Model Execution {modelDB.name} ended", "Execution ended!")
                mailTemplate.sendMail()
            return jsonify(model=model_schema.dump(modelDB))
        raise NotAllowedError("User not allowed to edit it")

    @jwt_required()
    def get(self, modelId):
        current_username = get_jwt_identity() # Get username from current user
        model = Model.query.filter_by(id=modelId).first() # Get model
        user = Users.query.filter_by(username=current_username).first()
        if model == None:
            raise NotFoundError("Model not found") 
        if user != None and (model.user.username == current_username or user.isadmin):
            return jsonify(model=model_schema.dump(model))
        raise NotAllowedError("User not allowed to access it")
    
    @jwt_required()
    def delete(self, modelId):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        model = Model.query.filter_by(id=modelId).first() # Get model
        if model == None:
            raise NotFoundError("Model not found") 
        if user != None and (user.isadmin or model.user.username == current_username):
            db.session.delete(model)
            db.session.commit()
            return jsonify(modelId=modelId)
        raise NotAllowedError("User not allowed to delete it")