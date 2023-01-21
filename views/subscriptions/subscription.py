from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
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

# Create the User and Subscriptions classes


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


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    current_plan = Column(String)
    plan_amount = Column(Float)
    card_number = Column(String)
    created_at = Column(Date)
    user = relationship("User", backref="subscriptions")


# Base.metadata.create_all(engine)
subscription = Blueprint('subscription', __name__)


@subscription.route('/subscription', methods=['POST'])
@jwt_required()
def user_subscription():
    user_id = get_jwt_identity()

    user_subscriptions = session.query(Subscriptions.id, Subscriptions.current_plan, Subscriptions.plan_amount,
                                       Subscriptions.card_number, Subscriptions.created_at).\
        filter_by(user_id=user_id).all()
    if not user_subscriptions:
        return jsonify({'error': 'Subscription not found'}), 404

    users_subscriptions = []
    for sub in user_subscriptions:
        sub_dict = {
            'id': sub.id,
            'current_plan': sub.current_plan,
            'plan_amount': sub.plan_amount,
            'card_number': sub.card_number,
            'created_at': sub.created_at,
        }
        users_subscriptions.append(sub_dict)
    return jsonify({'user_subscriptions': users_subscriptions})


