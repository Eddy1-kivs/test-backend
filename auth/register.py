import json
import sqlite3

from flask import Flask, request, jsonify, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime

get_started = Blueprint('get_started', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@get_started.route("/register", methods=["GET", 'POST'])
def signup():
    errors = {}
    requiredFields = ['first_name', 'last_name', 'phone_number', 'username', 'email', 'password', 'location']
    data = request.get_json()
    for field in requiredFields:
        if field not in data:
            errors[field] = 'This field is required'

    defaultValue = ''
    firstName = data.get('first_name', defaultValue)
    lastName = data.get('last_name', defaultValue)
    phoneNumber = data.get('phone_number', defaultValue)
    username = data.get('username', defaultValue)
    email = data.get('email', defaultValue)
    password = data.get('password', defaultValue)
    location = data.get('location', defaultValue)
    img = data.get('img', defaultValue)
    created_at = data.get('created_at', defaultValue)
    updated_at = data.get('updated_at', defaultValue)
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (first_name, last_name, phone_number, username, email, password, location, img, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
                       (firstName, lastName, phoneNumber, username, email, password, location, img, created_at, updated_at))
        conn.commit()
        return {'success': 'User has been registered'}
    except sqlite3.Error as e:
        print(e)
        return {'error': 'There was an error inserting the data'}
