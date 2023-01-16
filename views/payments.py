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
stripe.api_key = "pk_test_51MJWptKo6hjiMLcCn4CA6v4TEGkLzRzZ4r2rr3b93wLsPZ35YV0suqbcnQ3" \
                 "LZKMsQZtuOC8gPQNj4ejE5ZzB7zql00RjNbHXD4"

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

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
def charge():
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

    # retrieve the user's subscription details
    user_subscription = session.query(Subscriptions).filter_by(user_id=user_id).first()
    if not user_subscription:
        return jsonify({'error': 'Subscription not found'}), 404

    plan_amount = user_subscription.plan_amount

    # create a new charge using Stripe
    try:
        charge = stripe.Charge.create(
            amount=plan_amount,
            currency='usd',
            source=card_number,
            description='Example charge'
        )
    except Exception as e:
        return {"error": "Error creating Stripe token: {}".format(e)}
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            card={
                "number": card_number,
                "exp_month": int(expiration_date.split("/")[0]),
                "exp_year": int(expiration_date.split("/")[1]),
                "cvc": cvv,
                "name": card_holder_name
            },
            description='Charge for ' + username
        )
    except stripe.error.CardError as e:
        return {"error": e.json_body['error']['message']}

    # Save the payment details to the database
    payment = Payment(user_id=user_id,
                      card_number=card_number,
                      card_holder_name=card_holder_name,
                      expiration_date=expiration_date,
                      cvv=cvv,
                      amount=amount,
                      created_at=datetime.utcnow())
    session.add(payment)
    session.commit()

    return jsonify({'message': 'Payment successful'}), 200
