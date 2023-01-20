from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True, poolclass=QueuePool, pool_size=5, max_overflow=10)
Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))
session.close()


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

    # Base.metadata.create_all(bind=engine)


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
@jwt_required()
def users():
    user = get_jwt_identity()
    if not user:
        return jsonify({"msg": "Invalid user"}), 302
    user = session.query(User.id, User.username, User.email, User.first_name, User.last_name, User.location,
                         User.phone_number).filter_by\
        (id=user).first()
    session.close()
    if not user:
        return jsonify({'user': 'user does not exist'}), 302
    user_dict = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'location': user.location,
        'phone_number': user.phone_number
    }
    return jsonify({'user': user_dict})



