from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import re
from flask_session import Session
from flask import session
from datetime import datetime
from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
# app.config['SESSION_TYPE'] = 'sqlalchemy'
# app.config['SESSION_SQLALCHEMY'] = engine
# Session(app)
# Create the User class


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    location = Column(String)
    img = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)


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
    access_token = create_access_token(identity=user.username)
    user_data = {
        'username': user.username,
        'email': user.email,
        # 'first_name': user.first_name,
        # 'last_name': user.last_name
    }
    return jsonify(access_token=access_token, user_data=user_data)

