from flask import Flask, request, jsonify, session, Blueprint, redirect
import sqlite3
from flask_session import Session

sign_in = Blueprint('sign_in', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@sign_in.route("/login", methods=["GET", 'POST'])
def login():
    errors = {}
    requiredFields = ['username', 'password']

    for field in requiredFields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    defaultValue = ''
    username = request.get_json().get('username', defaultValue)
    password = request.get_json().get('password', defaultValue)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    if user is None:
        errors['username'] = 'Invalid username or password'
        return {'errors': errors}
    else:
        # log the user in and redirect to the home page
        session['user_id'] = user[0]
        return redirect('/home')

