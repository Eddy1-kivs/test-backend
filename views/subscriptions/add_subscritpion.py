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

stripe.api_key = "pk_test_51MJWptKo6hjiMLcCn4CA6v4TEGkLzRzZ4r2rr3b93wLsPZ35YV0suqbcnQ3" \
                 "LZKMsQZtuOC8gPQNj4ejE5ZzB7zql00RjNbHXD4"

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


@subscription.route('/subscription/add', methods=['POST'])
@jwt_required
def add_subscription():
    user_id = get_jwt_identity()
    # retrieve the subscription details from the request body
    current_plan = request.get_json().get('current_plan')
    plan_amount = request.get_json().get('plan_amount')
    card_number = request.get_json().get('card_number')
    created_at = datetime.utcnow()

    # create a new subscription object
    new_subscription = Subscriptions(user_id=user_id,
                                     current_plan=current_plan,
                                     plan_amount=plan_amount,
                                     card_number=card_number,
                                     created_at=created_at)
    # add the subscription to the session
    session.add(new_subscription)
    # commit the transaction
    session.commit()

    return jsonify({'message': 'New subscription added successfully.'})

