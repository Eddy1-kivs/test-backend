"""
user login blueprint

"""
import bcrypt
import re
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta
from models import *

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# jwt = JWTManager(app)


sign_in = Blueprint('sign_in', __name__)


@sign_in.route("/login", methods=["POST"])
def login():
    errors = {}
    required_fields = ['username', 'password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    username = request.get_json().get('username')
    password = request.get_json().get('password')

    user = session.query(User).filter_by(username=username).first()
    if user:
        # Compare password
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            user = user

            exp_time = datetime.utcnow() + timedelta(hours=2)
            expires_delta = exp_time - datetime.utcnow()
            token = create_access_token(identity=user.id, expires_delta=expires_delta)

            user = {
                'id': user.id,
                'username': user.username,
            }
            return jsonify(token=token, user=user, expires_delta=exp_time), 200
        else:
            errors['password'] = 'Invalid password'
            return jsonify(errors), 400
    else:
        errors['username'] = 'Invalid username'
        return jsonify(errors), 400
