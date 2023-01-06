import sqlite3
from flask import Blueprint, request, jsonify

logout = Blueprint('logout', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@logout.route('/logout', methods=['POST'])
def logout_user():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username=? AND password=?
    ''', (username, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Invalidate the user's session or token here
    # ...

    return jsonify({'success': True})
