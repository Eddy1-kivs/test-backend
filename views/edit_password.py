import sqlite3
import bcrypt
from flask import Blueprint, request, jsonify, session

change_password = Blueprint('change_password', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@change_password.route('/password-change', methods=['POST'])
def change_your_password():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized access'}), 401

    errors = {}
    required_fields = ['current_password', 'new_password', 'confirm_password']
    for field in required_fields:
        if not request.form.get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if new_password != confirm_password:
        return jsonify({'error': 'New password and confirm password do not match'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE id=?
    ''', (session.get('user_id'),))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid user'}), 401

    if not bcrypt.checkpw(current_password.encode('utf-8'), user[2].encode('utf-8')):
        return jsonify({'error': 'Invalid current password'}), 401

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute('''
        UPDATE users SET password=? WHERE id=?
    ''', (hashed_password, session.get('user_id')))
    conn.commit()

    return jsonify({'success': True})
