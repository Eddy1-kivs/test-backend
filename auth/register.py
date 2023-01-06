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
    requiredFields = ['first_name', 'last_name', 'phone_number', 'username',                      'email', 'password', 'location']
    for field in requiredFields:
        if field not in request.form:
            errors[field] = 'This field is required'

    defaultValue = ''
    firstName = request.form.get('first_name',    defaultValue)
    lastName = request.form.get('last_name', defaultValue)
    phoneNumber = request.form.get('phone_number', defaultValue)
    username = request.form.get('username', defaultValue)
    email = request.form.get('email', defaultValue)
    password = request.form.get('password', defaultValue)
    location = request.form.get('location', defaultValue)
    img = request.form.get('img', defaultValue)
    created_at = request.form.get('created_at', defaultValue)
    updated_at = request.form.get('updated_at', defaultValue)
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
