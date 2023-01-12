import json
import sqlite3
import datetime

from flask import Flask, request, jsonify, session, Blueprint

get_started = Blueprint('get_started', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@get_started.route("/register", methods=["POST"])
def signup():
    errors = {}
    required_fields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'location']
    for field in required_fields:
        if not request.form.get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone_number = request.form.get('phone_number')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    location = request.form.get('location')
    img = request.form.get('img', '')
    created_at = datetime.datetime.utcnow().isoformat()
    updated_at = created_at

    conn = get_db()
    cursor = conn.cursor()

    # Check if the provided username or email are already in use
    cursor.execute('SELECT id FROM users WHERE username=? OR email=?', (username, email))
    user = cursor.fetchone()
    if user:
        return jsonify({'error': 'Username or email already in use'}), 400

    try:
        cursor.execute('INSERT INTO users (first_name, last_name, phone_number, username, email,'
                       ' password, location, img, created_at, updated_at)'
                       ' VALUES (?,?,?,?,?,?,?,?,?,?)',
                       (first_name, last_name, phone_number, username, email, password, location, img, created_at,
                        updated_at))
        conn.commit()
        return {'success': 'User has been registered'}
    except sqlite3.Error as e:
        return {'error': 'There was an error inserting the data'}
