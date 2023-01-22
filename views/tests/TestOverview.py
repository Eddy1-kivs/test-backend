from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import scoped_session
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True, poolclass=QueuePool, pool_size=5, max_overflow=10)
Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))
session.close()


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
    start_date = Column(String)
    total_runs = Column(String)
    last_run = Column(String)
    user = relationship("User", backref="tests")

    # Base.metadata.create_all(engine)


overview = Blueprint('overview', __name__)


@overview.route('/test-overview', methods=['POST'])
@jwt_required()
def test_overview():
    user_id = get_jwt_identity()
    user_tests = session.query(Tests.id, Tests.test_url, Tests.start_date, Tests.total_runs, Tests.last_run).filter_by(id=user_id).all()
    if not user_tests:
        return jsonify({'tests': 'No tests found for this user.'})
    user_tests_list = []
    for test in user_tests:
        test_dict = {
            'id': test.id,
            'test_url': test.test_url,
            'start_date': test.start_date,
            'total_runs': test.total_runs,
            'last_run': test.last_run,
        }
        user_tests_list.append(test_dict)
    return jsonify(user_tests_list)


@overview.route('/delete-test', methods=['DELETE'])
@jwt_required()
def delete_test():
    user_id = get_jwt_identity()
    test_id = request.args.get('id')
    if not test_id:
        return jsonify({'error': 'Missing test_id'}), 400

    test = session.query(Tests).filter_by(user_id=user_id, id=test_id).first()
    if not test:
        return jsonify({'error': 'Invalid test_id'}), 401

    try:
        session.delete(test)
        session.commit()
        return jsonify({'message': 'Test deleted successfully'}), 200
    except:
        return jsonify({'error': 'Error in deleting test'}), 500



