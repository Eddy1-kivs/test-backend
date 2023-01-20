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


update_image = Blueprint('update_image', __name__)


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


@update_image.route('/edit-image', methods=['POST'])
@jwt_required()
def update_user_image():
    user_id = get_jwt_identity()
    errors = {}

    img = request.files.get('img')

    image_file_path = save_image(img)

    session.query(User).filter(User.id == user_id).update({
        'img': img,
    })
    session.commit()
    return jsonify({'success': True})
