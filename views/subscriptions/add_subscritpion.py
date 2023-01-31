from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
import stripe
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from config import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

stripe.api_key = "pk_test_51MJWptKo6hjiMLcCn4CA6v4TEGkLzRzZ4r2rr3b93wLsPZ35YV0suqbcnQ3" \
                 "LZKMsQZtuOC8gPQNj4ejE5ZzB7zql00RjNbHXD4"


add_subscription = Blueprint('add_subscription', __name__)


@add_subscription.route('/process_payment', methods=['POST'])
@jwt_required
def process_payment():
    plan_id = request.get_json().get('plan_id')
    subscription = session.query(Subscriptions).filter_by(id=plan_id).first()
    plan_amount = subscription.plan_amount
    if not payment:
        return jsonify({'message': 'Invalid payment method.'}), 400

    # Retrieve the subscription plan amount
    subscription = session.query(Subscriptions).filter_by(user_id=user_id).first()
    plan_amount = subscription.plan_amount

    # Process the payment using Stripe
    try:
        charge = stripe.Charge.create(
            amount=plan_amount,
            currency='usd',
            source=payment.card_number,
            description='Payment for subscription plan'
        )
        return jsonify({'message': 'Payment processed successfully.'})
    except stripe.error.CardError as e:
        return jsonify({'message': e.json_body['error']['message']}), 400


@add_subscription.route('/payment_methods', methods=['GET'])
@jwt_required()
def payment_queries():
    user_id = get_jwt_identity()
    payments = session.query(Payments.id, Payments.card_number, Payments.card_holder_name, Payments.expiration_date,
                             Payments.cvv).filter_by(user_id=user_id).all()
    subscription = session.query(Subscriptions.id, Subscriptions.current_plan, Subscriptions.plan_amount).filter_by\
        (user_id=user_id).first()
    return jsonify(payments=payments, subscription=subscription)
