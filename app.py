import os
# import psycopg2
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask_restful import Api
from database import db, ma
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from routes.test.HomeResource import HomeResource
from ressources.auth.UserRegisterResource import UserRegisterResource
from ressources.auth.UserLoginResource import UserLoginResource
from ressources.models.ModelResource import ModelResource
from ressources.models.ModelListResource import ModelListResource
load_dotenv()
app = Flask(__name__)
url = os.getenv('DATABASE_URL')
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = url
# initialize the app with the extension
db.init_app(app)
ma.init_app(app)
api = Api(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
# connection = psycopg2.connect(url)

api.add_resource(HomeResource, '/')
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(ModelResource, '/model')
api.add_resource(ModelListResource, '/models')

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    jwt = get_jwt()
    print(jwt)
    return jsonify(logged_in_as=current_user), 200
