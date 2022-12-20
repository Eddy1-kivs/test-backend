from flask import Flask, request, jsonify, session, Blueprint, make_response
from config.database import *
import jwt
import datetime

sign_in = Blueprint('sign_in', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)

    return decorated


@sign_in.route('/')
@sign_in.route('/login', methods=['POST', 'GET'])
def login():
    auth = request.form.get('username')
    login_error = {}
    if auth == 'POST' and 'user_name' in request.form and 'password' in request.form:
        username = request.form[StringField('username')]
        password = request.form[StringField('password')]
        cur = db.connection.cursor(db.cursors.DictCursor)
        db.execute('SELECT * FROM main.users WHERE users.username =%s AND password = %s', (user_name, password))
        users = cur.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['user_name'] = users['user_name']
        else:
            login_error['user'] = 'incorrect username/password'
            return jsonify({'login_error': login_error}), 401
        auth = jwt.encode({'user': auth, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': auth})

