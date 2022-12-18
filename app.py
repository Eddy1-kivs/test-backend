from flask import Flask, request, jsonify
import sqlite3
import os
import psycopg2
from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)


# app.config.from_prefixed_env()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////TestLoad.sqlite'
# db = 'TestLoad.sqlite'


# class UsersTable(db.TestLoad):
# id = db.column(db.Integer, primary_key=True)

# def user_auth(user):
#     return user


# class User:
#     def __init__(self, first_name, last_name,
#                  phone_number, username, email,
#                  password, created_at, updated_at,
#                  img, location):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.phone_number = phone_number
#         self.username = username
#         self.email = email
#         self.password = generate_password_hash(password, methods='sha256')
#         self.created_at = created_at
#         self.updated_at = updated_at
#         self.img = img
#         self.location = location
#
#     @classmethod
#     def authenticate(cls, **kwargs):
#         username = kwargs.get('username')
#         password = kwargs.get('password')
#         email = kwargs.get('email')
#         if not username or not password or not email:
#             return None
#         if not user or not check_password_hash(user.password, password):
#             return None
#         pass
#
#     def edit_email(self, email):
#         self.email = email
#         if not email:
#             return None
#
#     def edit_password(self, password):
#         self.password = generate_password_hash(password, methods='sha256')
#         pass
#
#     def edit_profile_picture(self, img):
#         self.img = img
#         pass
#
#     def to_dict(self):
#         return dict(**data)

# class Db:
#     connection = ''
#     curser = ''
#
#     def __init__(self):
#         self.connection = sqlite3.connect('TestLoad.sqlite')
#         self.curser = self.connection.cursor()
#
#     def find_or_create(self, table, column, value):
#         self.curser.execute("SELECT id FROM ? WHERE ?=? LIMIT 1", (table, column, value))
#         records = self.curser.fetchall()
#         if records.count() == false:
#             self.curser.execute("INSERT INTO users VALUES(main.users.username, main.users.username, main.users.first_name)")
#             self.curser.execute("SELECT id FROM ? WHERE ?=? LIMIT 1", (table, column, value))
#         return records


# cur = sqlite3.connect('TestLoad.sqlite')
# cur.close()


# SECRET_KEY = 'my_secret_Key'
# db = 'TestLoad.sqlite'
# @app.route('/', methods=['POST', 'GET'])
# def register():
#     data = request.get_data()
#     user = User.to_dict(**data)
#     cur = conn.cursor()
#     cur.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#                 (first_name, last_name,
#                  phone_number, username,
#                  email, password, created_at,
#                  updated_at, img, location))
#
#     db.commit()
#     return jsonify({'data'})


# @app.route('/', methods=['GET', 'POST'])
# def sign_in():
#     data = request.get_json(force=True, silent=True, cache=True)
#     login = user.authenticate(**data)
#
#     if not users:
#         return jsonify({'msg': 'Invalid credentials', 'authenticated': False}), 401
#
#     token = jwt.encode({
#         'sub': users.username,
#         'iat': datetime.utcnow(),
#         'exp': datetime.utcnow() + datetime.timedelta(hours=1)},
#         current_app.config['SECRET_KEY'])
#     return jsonify({'token': token.decode('UTF-8')})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
