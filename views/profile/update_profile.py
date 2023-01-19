from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import re
import datetime
import os
import phonenumbers
import uuid
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db')
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


update_profile = Blueprint('update_profile', __name__)


def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    return True


def save_image(image):
    if not image:
        return None
    try:
        file_ext = os.path.splitext(image.filename)[1]
        file_name = f"{str(uuid.uuid4())}{file_ext}"
        file_path = os.path.join("/images/", file_name)
        image.save(file_path)
    except:
        return None
    return file_path


@update_profile.route('/edit-profile', methods=['POST'])
@jwt_required()
def update_user_profile():
    user_id = get_jwt_identity()

    errors = {}
    required_fields = ['first_name', 'last_name', 'phone_number']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    img = request.files.get('img')
    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    location = request.get_json().get('location')
    phone_number = request.get_json().get('phone_number')
    if not validate_phone_number(phone_number):
        errors['phone_number'] = 'Invalid phone number'
    updated_at = datetime.now()

    if errors:
        return jsonify(errors), 400

    # Save the image to disk and retrieve the image file path
    image_file_path = save_image(img)

    # update the user profile
    session.query(User).filter(User.id == user_id).update({
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'location': location,
        'img': img,
        'updated_at': updated_at
    })
    session.commit()
    return jsonify({'success': True})

