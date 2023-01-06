import sqlite3
from flask import Blueprint, request, jsonify

change_email = Blueprint('change_email', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@change_email.route('/email-change', methods=['POST'])
def change_your_email():
    username = request.form.get('username')
    password = request.form.get('password')
    new_email = request.form.get('new_email')

    if not username or not password or not new_email:
        return jsonify({'error': 'Missing username, password, or new email'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username=? AND password=?
    ''', (username, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    cursor.execute('''
        UPDATE users SET email=? WHERE username=?
    ''', (new_email, username))
    conn.commit()

    return jsonify({'success': True})
