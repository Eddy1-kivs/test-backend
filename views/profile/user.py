from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

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


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
@jwt_required()
def user_profile():
    user_id = get_jwt_identity()
    user = session.query(User).filter_by(id=user_id).all()
    print(user)
    if not user:
        return jsonify({'user': 'user does not exist'})
    return jsonify({'user': [user.__dict__ for user in user]})
