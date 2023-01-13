import json
import sqlite3
import datetime
import bcrypt
from flask import Flask, request, jsonify, session, Blueprint

get_started = Blueprint('get_started', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@get_started.route("/register", methods=["POST"])
def signup():
    errors = {}
    required_fields = ['username', 'email', 'password', 'password_confirmation']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    username = request.get_json().get('username')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    password_confirmation = request.get_json().get('password_confirmation')
    created_at = datetime.datetime.utcnow().isoformat()

    if password != password_confirmation:
        return jsonify({'error': 'Passwords do not match'}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Check if the provided username or email are already in use
    cursor.execute('SELECT id FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user:
        errors['username'] = 'Username already in use'
    cursor.execute('SELECT id FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    if user:
        errors['email'] = 'Email already in use'
    if errors:
        return jsonify(errors), 400

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute('INSERT INTO users (username, email,'
                       ' password, created_at)'
                       ' VALUES (?,?,?,?)',
                       (username, email, hashed_password, created_at,))
        conn.commit()
        session['user_id'] = user[0]
        return {'success': 'User has been registered'}
    except sqlite3.Error as e:
        return {'error': 'There was an error inserting the data'}
