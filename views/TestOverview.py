from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Create the User and Tests classes
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

class Tests(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    username = Column(String)
    location = Column(String)
    browser = Column(String)
    test_url = Column(String)
    results = Column(String)
    user = relationship("User", backref="tests")


Base.metadata.create_all(engine)
overview = Blueprint('overview', __name__)


@overview.route('/test-overview', methods=['GET'])
@jwt_required
def test_overview():
    user_id = get_jwt_identity()
    user_tests = session.query(Tests).filter_by(user_id=user_id).all()
    if not user_tests:
        return jsonify({'tests': 'No tests found for this user.'})
    return jsonify({'tests': [test.__dict__ for test in user_tests]})



