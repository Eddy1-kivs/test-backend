import sqlite3
from flask import Blueprint, request, jsonify
import stripe
from auth.login import session

payments = Blueprint('payments', __name__)
stripe.api_key = "sk_test_51MJWptKo6hjiMLcCNyovmtJDXzqxc5xodOyEZsEXf0eYmUp3hFLy4LRq9DuQtKf6nogOdYj8LBMkomqYv3NrFx6C00lbMtZdxG"


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


def is_valid_card_number(card_number):
    # Add implementation to validate card number
    return True


def is_valid_expiration_date(expiration_date):
    # Add implementation to validate expiration date
    return True


def is_valid_cvv(cvv):
    # Add implementation to validate CVV
    return True


@payments.route("/charge", methods=["POST"])
def charge():
    user_id = session['user_id']
    # Get the payment details from the form
    username = request.form.get("username")
    card_number = request.form.get("card_number")
    card_holder_name = request.form.get("card_holder_name")
    expiration_date = request.form.get("expiration_date")
    cvv = request.form.get("cvv")
    amount = request.form.get("amount")

    # Validate the form input
    if not all([username, card_number, card_holder_name, expiration_date, cvv, amount]):
        return "Error: All fields are required"

    # Validate the card number
    if not is_valid_card_number(card_number):
        return "Error: Invalid card number"

    # Validate the expiration date
    if not is_valid_expiration_date(expiration_date):
        return "Error: Invalid expiration date"

    # Validate the CVV
    if not is_valid_cvv(cvv):
        return "Error: Invalid CVV"

    # Convert the amount to an integer and validate it
    try:
        amount = int(amount)
        if amount <= 0:
            return "Error: Invalid payment amount"
    except ValueError:
        return "Error: Invalid payment amount"

    # Get the database connection and cursor
    conn = get_db()
    cursor = conn.cursor()

    # Create a payment intent
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
        )
    except Exception as e:
        return "Error: {}".format(e)

    # Confirm the payment
    if payment_intent.status == "succeeded":
        # Payment successful, insert the payment details into the database
        try:
            cursor.execute(
                "INSERT INTO payments (username, card_number, card_holder_name, expiration_date, cvv) VALUES (?, ?, ?, ?, ?)",
                (username, card_number, card_holder_name, expiration_date, cvv))
            conn.commit()
        except Exception as e:
            return "Error inserting payment details: {}".format(e)

        return jsonify({
            "username": username,
            "card_number": card_number,
            "card_holder_name": card_holder_name,
            "expiration_date": expiration_date,
            "cvv": cvv
        })
    else:
        return "Error: Payment failed"