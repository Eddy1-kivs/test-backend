from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import re
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

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


change_email = Blueprint('change_email', __name__)


@change_email.route('/email-change', methods=['POST'])
@jwt_required
def change_your_email():
    user_id = get_jwt_identity()

    errors = {}
    required_fields = ['current_email', 'new_email_address', 'confirm_email', 'password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    current_email = request.get_json().get('current_email')
    new_email_address = request.get_json().get('new_email_address')
    confirm_email = request.get_json().get('confirm_email')
    password = request.get_json().get('password')

    if new_email_address != confirm_email:
        return jsonify({'error': 'New email address and confirm email address do not match'}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email_address):
        return jsonify({'error': 'Invalid email format'}), 400
    if new_email_address == current_email:
        return jsonify({'error': 'New email address is the same as current email'}), 400

    user = session.query(User).filter_by(user_id=user_id).one()
    if not user:
        return jsonify({'error': 'Invalid email'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'error': 'Invalid password'}), 401
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    edit_email = User(email=new_email_address)
    session.add(edit_email)
    session.commit()
    session.close()

    return jsonify({'success': True})
