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
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True, poolclass=QueuePool, pool_size=5, max_overflow=10)
Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))
session.close()


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
            user = user
            exp_time = datetime.utcnow() + timedelta(hours=2)
            token = create_access_token(identity=user.id)
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
