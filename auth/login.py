"""
user login blueprint

"""
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import re
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token), 200
        else:
            errors['password'] = 'Invalid password'
            return jsonify(errors), 400
    else:
        errors['username'] = 'Invalid username'
        return jsonify(errors), 400
