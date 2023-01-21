from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

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


change_password = Blueprint('change_password', __name__)


@change_password.route('/password-change', methods=['POST'])
@jwt_required()
def change_your_password():
    user = session.query(User).filter_by(id=get_jwt_identity()).one()
    errors = {}
    required_fields = ['current_password', 'new_password', 'confirm_password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 302

    current_password = request.get_json().get('current_password')
    new_password = request.get_json().get('new_password')
    confirm_password = request.get_json().get('confirm_password')

    if new_password != confirm_password:
        errors['confirm_password'] = 'New password and confirm password do not match'

    user = session.query(User).filter_by(id=user.id).one()
    if new_password == current_password:
        errors['new_password'] = 'New password should be different from the current password'
        if errors:
            return jsonify(errors)

    if not bcrypt.checkpw(current_password.encode('utf-8'), user.password):
        errors['current_password'] = 'Current password is incorrect'

        if errors:
            return jsonify(errors)

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed_password
    session.commit()
    session.close()

    return jsonify({'success': True})
