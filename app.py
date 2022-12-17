from flask import Flask, request, jsonify
import sqlite3


api = Flask(__name__)
# app.register_blueprint(new)
# app.register_blueprint(login)


class Db:
    connection = ''
    curser = ''

    def __init__(self):
        self.connection = sqlite3.connect('TestLoad.sqlite')
        self.curser = self.connection.cursor()

    def find_or_create(self, table, column, value):
        self.curser.execute("SELECT id FROM ? WHERE ?=? LIMIT 1", (table, column, value))
        records = self.curser.fetchall()
        if records.count() == false:
            self.curser.execute("INSERT INTO users VALUES(main.users.username, main.users.username, main.users.first_name)")
            self.curser.execute("SELECT id FROM ? WHERE ?=? LIMIT 1", (table, column, value))
        return records


# cur = sqlite3.connect('TestLoad.sqlite')
# cur.close()


SECRET_KEY = 'my_secret_Key'
# db = 'TestLoad.sqlite'


class Users:

    def __init__(self, first_name, last_name,
                 phone_number, username, email,
                 password, created_at, updated_at,
                 img, location):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, methods='sha256')
        self.created_at = created_at
        self.updated_at = updated_at
        self.img = img
        self.location = location

    @classmethod
    def authenticate(cls, **kwargs):
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        phone_number = kwargs.get("phone_number")
        username = kwargs.get('username')
        password = kwargs.get('password')
        email = kwargs.get('email')
        location = kwargs.get('location')
        created_at = kwargs.get('created_at')
        updated_at = kwargs.get('updated_at')
        img = kwargs.get('img')
        if not username or not password or not email:
            return None
        # user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None

    @staticmethod
    def to_dict():
        return dict(**data)


# @app.route('/', methods=['GET', 'POST'])
# def register():
#     data = request.get_json()
#     user = Users(**data)
#     cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
#     DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (user_name, password))
#     users = cur.fetchone()
#     return jsonify(user.to_dict()), 201
@api.route('/register', methods=['POST', 'GET'])
def register():
    data = request.get_json()
    user = Users(**data)
    conn = conn.cursor()
    conn.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                 (first_name, last_name,
                  phone_number, username,
                  email, password, created_at,
                  updated_at, img, location))

    db.commit()
    return jsonify(user.to_dict()), 201


class User(Db):

    # cur = sqlite3.connect(db)
    # curser.execute.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (user_name, password))
    # users = cur.fetchone()

    def __init__(self, username, email,
                 password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, methods='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        email = kwargs.get('email')
        if not username or not password or not email:
            return None
        user = cls.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    def to_dict(self):
        return dict(id=self.id, username=self.username)


@api.route('/', methods=['GET', 'POST'])
def sign_in():
    data = request.get_json()
    users = users.authenticate(**data)

    if not users:
        return jsonify({'msg': 'Invalid credentials', 'authenticated': False}), 401

    token = jwt.encode({
        'sub': users.username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + datetime.timedelta(hours=1)},
        current_app.config['SECRET_KEY'])
    return jsonify({'token': token.decode('UTF-8')})


if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=8000)
