import sqlite3
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


subscription = Blueprint('subscription', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@subscription.route('/subscription', methods=['GET'])
def user_subscription():
    user_id = get_jwt_identity()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
            SELECT * FROM subscriptions
            WHERE id=?
        ''', (user_id,))
    subscription = cursor.fetchone()
    if not subscription:
        return jsonify({'error': 'Subscription not found'}), 404

    return jsonify({
        'current_plan': subscription[1],
        'plan_amount': subscription[2],
        'card_number': subscription[3],
        'created_at': subscription[4],
    })
