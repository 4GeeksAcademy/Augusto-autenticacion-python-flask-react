"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, Blueprint, Flask
from api.models import User
from api.utils import APIException
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager, create_access_token
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app import app

CORS(app)
bcrypt = Bcrypt(app)

app = Flask(__name__)
api = Blueprint('api', __name__)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///path/to/your/database.db'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = '12345'
jwt = JWTManager(app)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def user_signup():
    try:
        user = User(
            email=request.json.get("email", None),
            password=bcrypt.generate_password_hash(request.json.get("password", None)).decode('utf-8'),
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        response_body = {
            "message": "Register Ok",
            "id": user.id,
            "email": user.email
        }
        return jsonify(response_body), 201
    except Exception as e:
        raise APIException(status_code=500, message=str(e))


@api.route("/login", methods=["POST"])
def login():

    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return jsonify({"msg": "Error email or password"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 201


@api.route("/private", methods=["GET"])
@jwt_required()
def protected():

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify(logged_in_as=current_user_id), 200

@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    api.run()