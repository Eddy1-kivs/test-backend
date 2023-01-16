from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

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


change_password = Blueprint('change_password', __name__)


@change_password.route('/password-change', methods=['POST'])
@jwt_required
def change_your_password():
    user_id = get_jwt_identity()
    errors = {}
    required_fields = ['current_password', 'new_password', 'confirm_password']
    for field in required_fields:
        if not request.form.get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    current_password = request.get_json().get('current_password')
    new_password = request.get_json().get('new_password')
    confirm_password = request.get_json().get('confirm_password')

    if new_password != confirm_password:
        return jsonify({'error': 'New password and confirm password do not match'}), 400

    user = session.query(User).filter_by(user_id=user_id).one()
    if not bcrypt.checkpw(current_password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'error': 'Invalid current password'}), 401

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password
    session.commit()
    session.close()

    return jsonify({'success': True})
