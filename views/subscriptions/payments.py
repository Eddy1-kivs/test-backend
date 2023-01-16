from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
import stripe

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

payments = Blueprint('payments', __name__)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    username = Column(String)
    card_number = Column(String)
    card_holder_name = Column(String)
    expiration_date = Column(Date)
    cvv = Column(String)
    created_at = Column(Date)
    user = relationship("User", backref="payments")


def is_valid_card_number(card_number):
    # Add implementation to validate card number using luhn algorithm
    if not card_number.isdigit():
        return False
    if not len(card_number) in (13, 15, 16):
        return False
    if not luhn(card_number):
        return False
    return True


def luhn(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10


def is_valid_expiration_date(expiration_date):
    # Add implementation to validate expiration date
    import datetime
    try:
        if datetime.datetime.strptime(expiration_date, '%m/%y') <= datetime.datetime.now():
            return False
    except ValueError:
        return False
    return True


def is_valid_cvv(cvv):
    # Add implementation to validate CVV
    if not cvv.isdigit():
        return False
    if not len(cvv) in (3, 4):
        return False
    return True


@payments.route("/charge", methods=["POST"])
@jwt_required
def card():
    user_id = get_jwt_identity()
    errors = {}
    required_fields = ['card_number', 'card_holder_name', 'expiration_date', 'cvv']
    for field in required_fields:
        if not request.form.get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    # Get the payment details from the form
    card_number = request.form.get("card_number")
    card_holder_name = request.form.get("card_holder_name")
    expiration_date = request.form.get("expiration_date")
    cvv = request.form.get("cvv")

    # Validate the form input
    if not all([card_number, card_holder_name, expiration_date, cvv]):
        return {"error": "All fields are required"}

    # Validate the card number
    if not is_valid_card_number(card_number):
        return {"error": "Invalid card number"}

    # Validate the expiration date
    if not is_valid_expiration_date(expiration_date):
        return {"error": "Invalid expiration date"}

    # Validate the CVV
    if not is_valid_cvv(cvv):
        return {"error": "Invalid CVV"}
    # Create the payment object
    payment = Payment(user_id=user_id, card_number=card_number, card_holder_name=card_holder_name,
                      expiration_date=expiration_date, cvv=cvv)
    session.add(payment)
    session.commit()

    return jsonify({'message': 'card added successfully'}), 200
