import os
# import psycopg2
from dotenv import load_dotenv
from flask import Flask
from flask import jsonify
from flask_restful import Api
from datetime import timedelta, datetime, timezone
from database import db, ma
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import logging
from routes.test.HomeResource import HomeResource
from ressources.auth.UserRegisterResource import UserRegisterResource
from ressources.auth.UserLoginResource import UserLoginResource
from ressources.models.ModelResource import ModelResource
from ressources.models.ModelListResource import ModelListResource
from ressources.admin.ListUsersResource import ListUsersResource
from ressources.admin.AdminResource import AdminResource
from ressources.admin.UserResource import UserResource
from ressources.admin.UserAdminResource import UserAdminResource
from models.Users import Users, user_schema
from errors.error import APIError
import traceback
import smtplib
from utils.mail import MailTemplate


load_dotenv()
app = Flask(__name__)
url = os.getenv('DATABASE_URL')
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = url
# initialize the app with the extension
db.init_app(app)
ma.init_app(app)
api = Api(app)
CORS(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

api.add_resource(HomeResource, '/')
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(ModelResource, '/model', '/model/<int:modelId>')
api.add_resource(ModelListResource, '/models')
api.add_resource(ListUsersResource, '/users')
api.add_resource(AdminResource, '/admin')
api.add_resource(UserResource, '/user', '/user/<int:userId>')
api.add_resource(UserAdminResource, '/admin/user/<int:userId>')

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

@app.route("/send_mail")
def index():
    mailTemplate = MailTemplate("corentinprp@gmail.com", "CVRP Test", "This is a test")
    mailTemplate.sendMail()
    return jsonify(status='ok')

# @app.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    user = Users.query.filter_by(username=identity).first() # Get user
    return jsonify(access_token=access_token, user=user_schema.dump(user))

# Exception handling
@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors 
    app.logger.error(f"{err.description}: {response['message']}")
    return jsonify(response), err.code

@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for any other server error"""
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = {"error": "Sorry, that error is on us, please contact support if this wasn't an accident"}
    return jsonify(response), 500

@app.errorhandler(404)
def handle_exception(err):
    """Return JSON instead of HTML for any other server error"""
    app.logger.error(f"Bad request: {str(err)}")
    response = {"error": "Bad request"}
    return jsonify(response), 404

if app.debug:
    logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    logging.getLogger().setLevel(logging.DEBUG)
    # Make sure engine.echo is set to False
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

