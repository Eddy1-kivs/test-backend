from flask import Flask, request, Blueprint, jsonify

app = Flask(__name__)
register = Blueprint('register', __name__)


@register.route('/', methods=['POST', 'GET'])
def new_user():
    auth = request.form
    register_error = {}
    if auth == 'POST' and 'first_name' in request.form \
            and 'user_name' in request.form and 'password' in \
            request.form and 'email' in request.form:
        first_name = request.form[StringField('first_name')]
        last_name = request.form[StringField('last_name')]
        phone_number = request.form[StringField('phone_number')]
        username = request.form[StringField('username')]
        email = request.form[StringField('email')]
        password = request.form[StringField('password')]
        created_at = request.form[StringField('created_at')]
        updated_at = request.form[StringField('updated_at')]
        img = Image.open('filename')
        img.save('filename.png')
        location = request.form[StringField('location')]

        cur = DATABASE.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (username, password))
        user = cur.fetchone()
        if user:
            register_error['user'] = 'already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            register_error['email'] = 'invalid email address'
        elif not re.match(r'[A-Za-z0-9]+', username):
            register_error['username'] = 'invalid username'
        elif not username or not password or not email:
            register_error['user'] = 'fill the form'
        else:
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (first_name, last_name,
                         phone_number, username,
                         email, generate_password_hash(password), created_at,
                         updated_at, img, location))

            DATABASE.commit()
            flash('You have successfully registered!')

            auth = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=
                                                                                                             30)})
            error = jwt.encode({'user': register_error})
            register_error = jsonify({'token': auth, 'error': register_error})
        return jsonify({'registered': auth})
    return jsonify({'error': register_error})
    # return make_response({'www.Authenticate': 'Basic realm="user already exists."'}, 401)


if __name__ == '__main__':
    app.run()

