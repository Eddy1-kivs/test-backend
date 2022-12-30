import json
from flask import Flask, request, jsonify, session, Blueprint
from flask_restful import Resource, Api
from config.database import db
from wtforms import StringField, FileField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import DataRequired, InputRequired
import wtforms_json
from werkzeug.utils import secure_filename


# wtforms_json.init()
# from flask_jwt_extended import (
#     jwt_required, create_access_token,
#     get_jwt_identity, get_jti
# )
# import bcrypt
# import time
# from logzero import logger
# import traceback

# app = Flask(__name__)
get_started = Blueprint('get_started', __name__)
api = Api(get_started)


@get_started.route('/register', methods=['POST', 'GET'])
def register():
    token = request.form
    if token == 'POST' and 'first_name' in request.form \
            and 'user_name' in request.form and 'password' in \
            request.form and 'email' in request.form:
        first_name = request.form[StringField('first_name', validators=[DataRequired()])]
        last_name = request.form[StringField('last_name', validators=[DataRequired()])]
        phone_number = request.form[StringField('phone_number', validators=[DataRequired()])]
        username = request.form[StringField('username', validators=[DataRequired()])]
        email = request.form[StringField('email', validators=[DataRequired()])]
        password = request.form[StringField('password', validators=[DataRequired()])]
        created_at = request.form[StringField('created_at', validators=[DataRequired()])]
        updated_at = request.form[StringField('updated_at', validators=[DataRequired()])]
        img = request.form[FileField('img', validators=[FileRequired()])]
        location = request.form[StringField('location', validators=[DataRequired()])]

        cur = db.cursor(DATABASE.cursors.DictCursor)
        db.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (username, password))
        user = cur.fetchone()

        error = {}

        if user:
            error['user'] = 'already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error['email'] = 'invalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            error['username'] = 'invalid username'
        elif not username or not password or not email:
            error['user'] = 'fill the form'
        else:
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (first_name, last_name,
                         phone_number, username,
                         email, password, created_at,
                         updated_at, img, location))

            db.commit()
            flash('You have successfully registered!')
            token = jwt.encode({'user': token.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=
                                                                                                              30)})
            error = jwt.encode({'user': error})
            # return jsonify({'token': token})
        return jsonify({'error': error})
    return jsonify({'token': token})

# api = Api(get_started)


# class UserRegistrationForm(FlaskForm):
#     first_name = StringField('first_name', validators=[InputRequired()])
#     last_name = StringField('last_name', validators=[InputRequired()])
#     phone_number = StringField('phone_number', validators=[InputRequired()])
#     username = StringField('username', validators=[InputRequired()])
#     email = StringField('email', validators=[InputRequired()])
#     password = StringField('password', validators=[InputRequired()])
#     location = StringField('location', validators=[InputRequired()])
#     img = FileField('img', validators=[FileRequired()])
#     created_at = StringField('created_at', validators=[InputRequired()])
#     updated_at = StringField('updated_at', validators=[InputRequired()])


# @get_started.route('/')
# def register():
#     form = UserRegistrationForm()
#     # if form.validate_on_submit():
#     #     return redirect('/success')
#     print(form)
#     return json.dumps(form)
#     # return {json}


# def convert_to_binary_data(filename):
#     with open(filename, 'rb') as file:
#         blob_data = file.read()
#     return blob_data


# @get_started.route('/')
# @get_started.route("/register", methods=["GET", "POST"])
# def signup():
#     if not request.get_json():
#         return jsonify({"message": "Missing JSON in request"}), 400
#     data = request.form
#     first_name = data[StringField('first_name', validators=[InputRequired()])]
#     last_name = data[StringField('last_name', validators=[InputRequired()])]
#     phone_number = data[StringField('phone_number', validators=[InputRequired()])]
#     username = data[StringField('username', validators=[InputRequired()])]
#     email = data[StringField('email', validators=[InputRequired()])]
#     password = data[StringField('password', validators=[InputRequired()])]
#     location = data[StringField('location', validators=[InputRequired()])]
#     img = data(convert_to_binary_data(['img']))
#     created_at = data[StringField('created_at', validators=[InputRequired()])]
#     updated_at = data[StringField('updated_at', validators=[InputRequired()])]
#
#     print(f'signup request: username={username}, password={password}')
#
#     if username and username.encode().isalnum():
#         return json.dumps({"mode": "signup", "status": "error", "message": "Format does not match"}), 400
#
#     cur = db.connection.cursor(db.cursors.DictCursor)
#     db.execute('SELECT * FROM main.users  WHERE username=?;')
#     users: object = cur.fetchone()
#     if db[username]:
#         return json.dumps({"mode": "signup", "status": "error", "message": "This username cannot be used since it already exist"}), 400
#
#     salt = bcrypt.gensalt(rounds=10, prefix=b"2a")
#     hashed_pass = bcrypt.hashpw(password.encode(), salt).decode()
#     cur = conn.cursor()
#     cur.execute("INSERT INTO main.users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",)
#     db.commit()
#     db(username, hashed_pass)
#     return json.dumps({"mode": "signup", "status": "success", "message": "Completed"}), 200


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
