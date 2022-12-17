from flask import Flask, request, Blueprint, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
new = Blueprint('new', __name__)


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

    def to_dict(self):
        return dict(id=self.id, username=self.username)


# @app.route('/', methods=['GET', 'POST'])
# def register():
#     data = request.get_json()
#     user = Users(**data)
#     cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
#     DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (user_name, password))
#     users = cur.fetchone()
#     return jsonify(user.to_dict()), 201
@app.route('/')
def register():
    data = request.get_json()
    user = Users(**data)
    return jsonify({'user.to_dict'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


