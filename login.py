from flask import Flask, request, Blueprint, jsonify, jsonify, request, current_app
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash
from datetime import datetime
# from app import DATABASE


app = Flask(__name__)
login = Blueprint('login', __name__)

DATABASE = TestLoad.sqlite


class User(DATABASE.tables):

    # cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
    # DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (user_name, password))
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


@app.route('/', methods=['GET', 'POST'])
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
    app.run(debug=True, host='0.0.0.0', port=8080)



