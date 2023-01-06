import sqlite3
from flask import Blueprint, request, jsonify

change_password = Blueprint('change_password', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@change_password.route('/change-password', methods=['POST'])
def change_your_password():
    username = request.form.get('username')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({'error': 'Missing username, old password, or new password'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username=? AND password=?
    ''', (username, old_password))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    cursor.execute('''
        UPDATE users SET password=? WHERE username=?
    ''', (new_password, username))
    conn.commit()

    return jsonify({'success': True})
