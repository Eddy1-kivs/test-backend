from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token
import bcrypt
import bcrypt
import sqlite3

sign_in = Blueprint('sign_in', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@sign_in.route("/login", methods=["POST"])
def login():
    errors = {}
    required_fields = ['username', 'password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    username = request.get_json().get('username')
    password = request.get_json().get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if user is None:
        errors['username'] = 'Invalid username or password'
        return jsonify(errors), 400
    else:
        # Compare password
        if not bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            errors['password'] = 'Invalid username or password'
            return jsonify(errors), 400

    # log the user in by creating a JWT
    access_token = create_access_token(identity=user[0])
    return jsonify(access_token=access_token), 200
