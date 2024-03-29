import bcrypt
import re
from flask_session import Session
from flask import session
from datetime import datetime
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, Blueprint
from models import *
from flask_jwt_extended import JWTManager, create_access_token

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# jwt = JWTManager(app)


get_started = Blueprint('get_started', __name__)


# Create the /register endpoint
@get_started.route("/register", methods=["POST"])
def signup():
    errors = {}
    required_fields = ['username', 'email', 'password', 'password_confirmation']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    email = request.get_json().get('email')
    if email:
        # Check if email is in the correct format
        match = re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
        if not match:
            errors['email'] = 'Invalid email format'
    if errors:
        return jsonify(errors), 400
    username = request.get_json().get('username')
    if username:
        # Check if username is in the correct format
        match = re.match(r'^[a-zA-Z0-9_]+$', username)
        if not match:
            errors['username'] = 'Invalid username format'

        if len(username) < 4 or len(username) > 20:
            errors['username'] = 'Username must be between 4 and 20 characters'

        if errors:
            return jsonify(errors), 400

    username = request.get_json().get('username')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    password_confirmation = request.get_json().get('password_confirmation')
    created_at = datetime.now()

    if password != password_confirmation:
        errors['passwords'] = 'passwords do not match'
        return jsonify(errors), 400

    user = session.query(User).filter_by(username=username).first()
    if user:
        errors['username'] = 'Username already in use'
    user = session.query(User).filter_by(email=email).first()
    if user:
        errors['email'] = 'Email already in use'
    if errors:
        return jsonify(errors), 400

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert new
    new_user = User(username=username, email=email, password=hashed_password, created_at=created_at)
    session.add(new_user)
    session.commit()
    user = new_user

    exp_time = datetime.utcnow() + timedelta(hours=2)
    expires_delta = exp_time - datetime.utcnow()
    token = create_access_token(identity=user.id, expires_delta=expires_delta)

    user = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }
    return jsonify(token=token, user=user, expires_delta=exp_time)
