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

stripe.api_key = "pk_test_51MJWptKo6hjiMLcCn4CA6v4TEGkLzRzZ4r2rr3b93wLsPZ35YV0suqbcnQ3" \
                 "LZKMsQZtuOC8gPQNj4ejE5ZzB7zql00RjNbHXD4"


payments = Blueprint('payments', __name__)

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


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_number = Column(String)
    card_holder_name = Column(String)
    expiration_date = Column(String)
    cvv = Column(String)
    created_at = Column(Date)
    user = relationship("User", backref="payments")


# Base.metadata.create_all(engine)
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


@payments.route("/add-card", methods=["POST"])
@jwt_required()
def charge():
    user_id = get_jwt_identity()
    errors = {}
    required_fields = ['card_holder_name', 'expiration_date', 'cvv', 'card_number']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    # Get the payment details from the form
    card_number = str(request.get_json().get("card_number"))
    card_holder_name = request.get_json().get("card_holder_name")
    expiration_date = request.get_json().get("expiration_date")
    cvv = str(request.get_json().get("cvv"))
    created_at = datetime.now()

    if not is_valid_card_number(card_number):
        errors['card_number'] = 'Invalid card number'

        # check if the expiration date is valid
    if not is_valid_expiration_date(expiration_date):
        errors['expiration_date'] = 'Invalid expiration date'

        # check if the cvv is valid
    if not is_valid_cvv(cvv):
        errors['cvv'] = 'Invalid CVV'

    if errors:
        return jsonify(errors), 400

    new_card = Payments(
        user_id=user_id,
        # username=username,
        card_number=card_number,
        card_holder_name=card_holder_name,
        expiration_date=expiration_date,
        cvv=cvv,
        created_at=datetime.now()
    )
    session.add(new_card)
    session.commit()

    card = new_card
    card = {
        'id': card.id,
        'card_number': card.card_number,
        'card_holder_name': card.card_holder_name,
        'expiration_date': card.expiration_date,
        'cvv': card.cvv,
        'created_at': card.created_at,
    }

    return jsonify(card=card)

