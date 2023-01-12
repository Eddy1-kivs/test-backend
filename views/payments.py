import sqlite3
from flask import Blueprint, request, jsonify
import stripe
from auth.login import session

payments = Blueprint('payments', __name__)
stripe.api_key = "pk_test_51MJWptKo6hjiMLcCn4CA6v4TEGkLzRzZ4r2rr3b93wLsPZ35YV0suqbcnQ3" \
                 "LZKMsQZtuOC8gPQNj4ejE5ZzB7zql00RjNbHXD4"


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


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
def charge():
    user_id = session['user_id']
    errors = {}
    required_fields = ['username', 'card_number', 'card_holder_name', 'expiration_date', 'cvv', 'amount']
    for field in required_fields:
        if not request.form.get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    # Get the payment details from the form
    username = request.form.get("username")
    card_number = request.form.get("card_number")
    card_holder_name = request.form.get("card_holder_name")
    expiration_date = request.form.get("expiration_date")
    cvv = request.form.get("cvv")
    amount = request.form.get("amount")

    # Validate the form input
    # if not all([username, card_number, card_holder_name, expiration_date, cvv, amount]):
    #     return {"error": "All fields are required"}

    # Validate the card number
    if not is_valid_card_number(card_number):
        return {"error": "Invalid card number"}

    # Validate the expiration date
    if not is_valid_expiration_date(expiration_date):
        return {"error": "Invalid expiration date"}

    # Validate the CVV
    if not is_valid_cvv(cvv):
        return {"error": "Invalid CVV"}

    # Convert the amount to an integer and validate it
    try:
        amount = int(amount)
        if amount <= 0:
            return {"error": "Invalid payment amount"}
    except ValueError:
        return {"error": "Invalid payment amount"}

    # Create a Stripe token from the card details
    try:
        token = stripe.Token.create(
            card={
                "number": card_number,
                "exp_month": expiration_date.split("/")[0],
                "exp_year": expiration_date.split("/")[1],
                "cvc": cvv,
                "name": card_holder_name
            },
        )
    except Exception as e:
        return {"error": "Error creating Stripe token: {}".format(e)}

    # Charge the payment
    try:
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token.id,
            description="Payment for {}".format(username)
        )
    except Exception as e:
        return {"error": "Error charging payment: {}".format(e)}

    # Check if the payment was successful
    if charge.status == "succeeded":
        # Payment successful, insert the payment details into the database
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO payments (username, card_number, card_holder_name, expiration_date, cvv) "
                "VALUES (?, ?, ?, ?, ?)",
                (username, "xxxx-xxxx-xxxx-" + card_number[-4:], card_holder_name, expiration_date, "xxx"))
            conn.commit()
        except Exception as e:
            return {"error": "Error inserting payment details: {}".format(e)}

        return {"username": username,
                "amount": amount,
                "status": "success"}
    else:
        return {"error": "Payment failed"}
