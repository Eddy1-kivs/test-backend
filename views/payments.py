import sqlite3
from flask import Blueprint, request, jsonify
import stripe

payments = Blueprint('payments', __name__)
stripe.api_key = "sk_test_51MJWptKo6hjiMLcCNyovmtJDXzqxc5xodOyEZsEXf0eYmUp3hFLy4LRq9DuQtKf6nogOdYj8LBMkomqYv3NrFx6C00lbMtZdxG"


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@payments.route("/charge", methods=["POST"])
def charge():
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

    # Convert the amount to an integer
    try:
        amount = int(amount)
    except ValueError:
        return "Error: Invalid payment amount"

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
        cursor.execute(
            "INSERT INTO payments (username, card_number, card_holder_name, expiration_date, cvv) VALUES (?, ?, ?, ?, ?)",
            (username, card_number, card_holder_name, expiration_date, cvv)
        )
        conn.commit()

        return jsonify({
            "username": username,
            "card_number": card_number,
            "card_holder_name": card_holder_name,
            "expiration_date": expiration_date,
            "cvv": cvv
        })
    else:
        return "Error: Payment failed"