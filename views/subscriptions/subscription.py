from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from models import *
app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


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


