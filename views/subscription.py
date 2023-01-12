import sqlite3
from flask import Blueprint, jsonify
from auth.login import session

subscription = Blueprint('subscription', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@subscription.route('/subscription', methods=['GET'])
def user_subscription():
    user_id = session['user_id']

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
