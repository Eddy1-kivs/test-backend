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
    required_fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'location',
                       'confirm_password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    phone_number = request.get_json().get('phone_number')
    username = request.get_json().get('username')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    confirm_password = request.get_json().get('confirm_password')
    location = request.get_json().get('location')
    created_at = datetime.datetime.utcnow().isoformat()
    updated_at = created_at

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Check if the provided username or email are already in use
    cursor.execute('SELECT id FROM users WHERE username=? OR email=?', (username, email))
    user = cursor.fetchone()
    if user:
        return jsonify({'error': 'Username or email already in use'}), 400

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf-8')

    try:
        cursor.execute('INSERT INTO users (first_name, last_name, phone_number, username, email,'
                       ' password, location, created_at, updated_at)'
                       ' VALUES (?,?,?,?,?,?,?,?,?,?)',
                       (first_name, last_name, phone_number, username, email, hashed_password, location, created_at,
                        updated_at))
        conn.commit()
        return {'success': 'User has been registered'}
    except sqlite3.Error as e:
        return {'error': 'There was an error inserting the data'}
