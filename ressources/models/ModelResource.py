from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ressources.models.ModelCVRPApi import ModelCVRPApi
from models.Users import Users
from models.Model import Model, model_schema
from database import db
import uuid
import json
import os

class ModelResource(Resource):
    @jwt_required()
    def post(self):
        current_username = get_jwt_identity() # Get username from current user
        user = Users.query.filter_by(username=current_username).first() # Get user
        model = ModelCVRPApi()
        model.readFromData(request.json['data'])
        model.initModel(request.json['parameters']['vehicle_max_capacity'])
        model.optimizeModel(request.json['parameters'])
        id = str(uuid.uuid4())
        model.modelGurobi.write(id + '.sol')
        # Store the model
        # Assign the model to the current user
        modelDB = Model()
        modelDB.name = 'Test'
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
        return jsonify(model=model_schema.dump(modelDB))

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity() # Get username from current user
        modelId = request.args.get('id')
        modelDB = Model.query.filter_by(id=modelId).first() # Get model
        parameters = request.json.get('parameters', None)
        if parameters is None:
            parameters = modelDB.parameters
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
        db.session.commit()
        print(model.getRoutesFromSolution())
        return jsonify(model=model_schema.dump(modelDB))

    @jwt_required()
    def get(self):
        current_username = get_jwt_identity() # Get username from current user
        modelId = request.args.get('id')
        model = Model.query.filter_by(id=modelId).first() # Get model
        if model == None:
            response = jsonify(error="Model not found")
            response.status_code = 404 # or 400 or whatever
            return response   
        if model.user.username == current_username:
            return jsonify(model=model_schema.dump(model))
        response = jsonify(error="User not allowed to access it")
        response.status_code = 401 # or 400 or whatever
        return response