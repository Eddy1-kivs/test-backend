import sqlite3
from flask import Blueprint, request, jsonify

subscription = Blueprint('subscription', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@subscription.route('/subscription', methods=['GET'])
def user_subscription():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM subscriptions WHERE username=?
    ''', username)
    subscription = cursor.fetchone()
    if not subscription:
        return jsonify({'error': 'Invalid username'}), 401

    return jsonify({
        'current_plan': subscription[1],
        'plan_amount': subscription[2],
        'card_number': subscription[3],
        'created_at': subscription[4],
    })
