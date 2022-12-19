from flask import Flask, request, jsonify, session, Blueprint
import sqlite3
import os
# import psycopg2
from dotenv import load_dotenv
from models.billingHistory import billing
from models.download import download_file
from models.EditEmail import email_edit
from models.EditPassword import password_change
from models.EditProfilePicture import profile_edit
from models.logout import out
from models.payment import pay
from models.subscription import subs
from models.TestOverview import overview
from auth.login import sign_in
# from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
# connection = psycopg2.connect(url)
conn = sqlite3.connect('TestLoad.sqlite')
conn.close()
db = 'TestLoad.sqlite'

app.register_blueprint(billing)
app.register_blueprint(download_file)
app.register_blueprint(email_edit)
app.register_blueprint(password_change)
app.register_blueprint(profile_edit)
app.register_blueprint(out)
app.register_blueprint(pay)
app.register_blueprint(subs)
app.register_blueprint(overview)
app.register_blueprint(sign_in)


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


# @app.route('/')
@app.route('/register', methods =['GET', 'POST'])
def register():
    data = request.get_json()
    if request.get_json() == 'POST':
        first_name = [StringField('first_name')]
        last_name = [StringField('last_name')]
        phone_number = [StringField('phone_number')]
        username = [StringField('username')]
        email = [StringField('email')]
        password = ['password']
        location = [StringField('location')]
        img = ['img']
        created_at = [StringField('created_at')]
        updated_at = [StringField('updated_at')]
        cur = db.cursor(db.cursors.DictCursor)
        db.execute('SELECT * FROM main.users WHERE users.username =%s AND password = %s', (username, password))
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
            cur.execute("INSERT INTO main.users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",)

            db.commit()
            token = jwt.encode({'user': data})
            error = jwt.encode({'user': error})
        return jsonify({'token': token})
        # return jsonify({"username": username, "message": f"user {username} created."}), 201
    return jsonify({'error': error})


@app.route('/')
@app.route('/Login', methods=['GET', 'POST'])
def login():
    auth = request.form
    login_error = {}
    if auth == 'POST' and 'user_name' in request.form and 'password' in request.form:
        user_name = request.form[StringField('username')]
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
            token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
            login_error = jwt.encode({'user': login_error})
            return jsonify({"token": token})
    return jsonify({"login_error": login_error})

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
# if __name__ == '__main__':
app.run(debug=True, host='0.0.0.0', port=8000)
