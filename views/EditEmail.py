import sqlite3
import bcrypt
from flask import Blueprint, request, jsonify, session

change_email = Blueprint('change_email', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@change_email.route('/email-change', methods=['POST'])
def change_your_email():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized access'}), 401

    errors = {}
    required_fields = ['current_email', 'new_email_address', 'confirm_email', 'password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    current_email = request.get_json().get('current_email')
    new_email_address = request.get_json().get('new_email_address')
    confirm_email = request.get_json().get('confirm_email')
    password = request.get_json().get('password')

    if new_email_address != confirm_email:
        return jsonify({'error': 'New email address and confirm email address do not match'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE email=?
    ''', (current_email,))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid email'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'error': 'Invalid password'}), 401
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute('''
        UPDATE users SET email=?, password=? WHERE email=?
    ''', (new_email_address, hashed_password, current_email))
    conn.commit()

    return jsonify({'success': True})

