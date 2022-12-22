import json
from flask import Flask, request, jsonify, session, Blueprint
from config.database import db
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_jti
)
import bcrypt
import time
from logzero import logger
import traceback

# app = Flask(__name__)
get_started = Blueprint('get_started', __name__)


def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


@get_started.route('/')
@get_started.route("/register", methods=["GET", "POST"])
def signup():
    if not request.get_json():
        return jsonify({"message": "Missing JSON in request"}), 400
    data = request.get_json()
    first_name = data[StringField('first_name', validators=[InputRequired()])]
    last_name = data[StringField('last_name', validators=[InputRequired()])]
    phone_number = data[StringField('phone_number', validators=[InputRequired()])]
    username = data[StringField('username', validators=[InputRequired()])]
    email = data[StringField('email', validators=[InputRequired()])]
    password = data[StringField('password', validators=[InputRequired()])]
    location = data[StringField('location', validators=[InputRequired()])]
    img = data(convert_to_binary_data(['img']))
    created_at = data[StringField('created_at', validators=[InputRequired()])]
    updated_at = data[StringField('updated_at', validators=[InputRequired()])]

    print(f'signup request: username={username}, password={password}')

    if username and username.encode().isalnum():
        return json.dumps({"mode": "signup", "status": "error", "message": "Format does not match"}), 400

    cur = db.connection.cursor(db.cursors.DictCursor)
    db.execute('SELECT * FROM main.users  WHERE username=?;')
    users = cur.fetchone()
    if db[username]:
        return json.dumps({"mode": "signup", "status": "error", "message": "This username cannot be used since it already exist"}), 400

    salt = bcrypt.gensalt(rounds=10, prefix=b"2a")
    hashed_pass = bcrypt.hashpw(password.encode(), salt).decode()
    cur = conn.cursor()
    cur.execute("INSERT INTO main.users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",)
    db.commit()
    db(username, hashed_pass)
    return json.dumps({"mode": "signup", "status": "success", "message": "Completed"}), 200


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
# @get_started.route('/')
# @get_started.route('/register', methods =['GET', 'POST'])
# def register():
#     data = request.get_json()
#     if request.get_json() == 'POST':
#         first_name = [StringField('first_name')]
#         last_name = [StringField('last_name')]
#         phone_number = [StringField('phone_number')]
#         username = [StringField('username')]
#         email = [StringField('email')]
#         password = ['password']
#         location = [StringField('location')]
#         img = ['img']
#         created_at = [StringField('created_at')]
#         updated_at = [StringField('updated_at')]
#         cur = db.cursor(db.cursors.DictCursor)
#         db.execute('SELECT * FROM main.users WHERE users.username =%s AND password = %s', (username, password))
#         user = cur.fetchone()
#
#         error = {}
#
#         if user:
#             error['user'] = 'already exists'
#         elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
#             error['email'] = 'invalid email address'
#         elif not re.match(r'[A-Za-z0-9]+', username):
#             error['username'] = 'invalid username'
#         elif not username or not password or not email:
#             error['user'] = 'fill the form'
#         else:
#             cur = conn.cursor()
#             cur.execute("INSERT INTO main.users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",)
#
#             db.commit()
#             token = jwt.encode({'user': data})
#             error = jwt.encode({'user': error})
#         return jsonify({'token': token})
#         # return jsonify({"username": username, "message": f"user {username} created."}), 201
#     return jsonify({'error': error})
