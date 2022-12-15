import datetime
import locale
import re
from functools import wraps
import jwt as jwt
from flask import Flask, request, jsonify, flash, make_response, session, send_file
import sqlite3
from wtforms import StringField, validators, SubmitField
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash

# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)

conn = sqlite3.connect('TestLoad.sqlite')
conn.close()

SECRET_KEY = 'my_secret_Key'

DATABASE = 'TestLoad.sqlite'


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


# Registration for new members
# when the new member fills out the form the database checks to see if they already exist
# if the member is not in the database he/she is added to the database
# else the member will be requested to log in


@app.route('/', methods=['POST', 'GET'])
def register():
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
        location = request.form[StringField('location', validators=[DataRequired()])]

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
    return jsonify({'registered': auth, 'error': register_error})

    # return make_response({'www.Authenticate': 'Basic realm="user already exists."'}, 401)


# Login page
# the user will fill the form with their credentials
# if the credentials are valid, the user will be logged in and redirected to home page
# if the credentials are invalid, the user will not be logged in.
# they will be required to fill out the login form again with valid credentials
#


@app.route('/', methods=['GET', 'POST'])
def login():
    auth = request.form
    login_error = {}
    if auth == 'POST' and 'user_name' in request.form and 'password' in request.form:
        user_name = request.form[StringField('username', validators=[DataRequired()])]
        password = request.form[StringField('password', validators=[DataRequired()])]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (user_name, password))
        users = cur.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['user_name'] = users['user_name']
            return 'logged in successfully'
        else:
            login_error['user'] = 'incorrect username/password'
            auth = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
            login_error = jwt.encode({'user': login_error})
    return jsonify({'login_error': login_error, 'login': auth})


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user_name', None)
    return 'logged out successfully'


@app.route('/EditEmailModal', methods=['GET', 'POST'])
def change_email(email_change):
    email = request.form
    if request.method == 'POST':
        email = request.form[StringField('Email', validators=[DataRequired()])]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('UPDATE users SET email = %s  WHERE email = %s', email)
        DATABASE.commit()
        flash('Your email address has been updated successfully')
        token = jwt.encode({'user': email.email})
        return jsonify({'token': token})
    return make_response('email update failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/EditPasswordModal', methods=['GET', 'POST'])
def change_password(change_your_password):
    password = request.form
    if request.method == 'POST':
        password = request.form[StringField('password', validators=[DataRequired()])]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('UPDATE users SET password = %s WHERE password = %s', password)
        DATABASE.commit()
        flash('Your password has been updated successfully')
        token = jwt.encode({'user': password.password})
        return jsonify({'token': token})
    return make_response('password update failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/EditProfilePicture', methods=['GET', 'POST'])
def change_profile(profile_change):
    img = request.form
    if request.method == 'POST':
        img = request.form[bytes('profile', validators=[DataRequired()])]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute(
            'UPDATE users SET username = %s, first_name = %s, last_name = %s, phone_number = %s  WHERE username = ?')
        DATABASE.commit()
        flash('Your profile has been updated successfully')
        token = jwt.encode({'user': profile_change['username', 'first_name', 'last_name', 'phone_number']})
        return jsonify({'token': token})
    return make_response('profile update failed', 401, {'www.Authenticate': 'Basic realm'})


class CurrencyCol:
    @staticmethod
    def td_format(content):
        amount = float(content.replace(',', ''))
        locale.setlocale(locale.LC_NUMERIC, 'nl_NL')
        val = locale.format_string('%.2f', float(amount), 1, 1).replace(' ', '.')
        return f'$ {val}'


class Number:
    def verify(self):
        number_string = self.replace("-", "")
        list_number = [int(n) for n in number_string]

        if not list_number[0] == 4:
            return False

        if not list_number[3] - list_number[4] == 1:
            return False

        if not sum(list_number) % 4 == 0:
            return False

        if not int(number_string[0:2]) + int(number_string[6:8]) == 100:
            return False

        return True


@app.route('/subscription', methods=['GET', 'POST'])
def subscription():
    subscribe = request.form
    if subscribe == 'POST' and 'username' in request.form and 'current_plan' in request.form and 'plan_amount' in request.form and 'card_number' in request.form and 'created_at' in request.form:
        username = request.form[StringField('username', validators=[DataRequired()])]
        current_plan = request.form[StringField('current_plan', validators=[DataRequired()])]
        plan_amount = request.form[CurrencyCol('plan_amount', validators=[DataRequired()])]
        card_number = request.form[Number('card_number', validators=[DataRequired()])]
        created_at = request.form[StringField('created_at', validators=[DataRequired()])]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        cur.execute("INSERT INTO subscriptions VALUES (%s,%s,%s,%s,%s,%s)",
                    (username, plan_amount,
                     card_number, created_at,
                     created_at))
        DATABASE.commit()
        flash('You have successfully subscribed!')
        token = jwt.encode({'subscriptions': username, 'exp': datetime.datetime.utcnow()})
        return jsonify({'token': token})
    return make_response('subscription failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/PaymentMethod', methods=['GET', 'POST'])
def add_payment():
    add = request.form
    if add == 'POST' and 'username' in request.form and 'card_number' in request.form and 'card_holder_name' in request.form and 'expiration_date' in request.form and 'cvv' in request.form:
        username = request.form[StringField('username', validators=[DataRequired()])]
        card_number = request.form[Number('card_number', validators=[DataRequired()])]
        card_holder_name = request.form[StringField('card_holder_name', validators=[DataRequired()])]
        expiration_date = request.form[StringField('expiration_date', validators=[DataRequired()])]
        cvv = request.form[StringField('cvv', validators=[DataRequired(), validators.length(min=3, max=3)])]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        cur.execute("INSERT INTO payments VALUES ( %s,%s,%s,%s,%s,%s)",
                    (username,
                     card_number,
                     card_holder_name,
                     expiration_date,
                     cvv))
        DATABASE.commit()
        flash('You have successfully added payment!')
        token = jwt.encode({'payments': username, 'exp': datetime.datetime.utcnow()})
        return jsonify({'token': token})
    return make_response('add payment failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/test-overview', methods=['GET', 'POST'])
def test():
    test_data = test
    msg = {}
    cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
    post = cur.execute('SELECT * FROM tests WHERE id = ?',
                       (test_data,)).fetchall()
    conn.close()
    if post is None:
        msg['billing_histories'] = 'No billing history'
        test_data = jwt.encode({'test': id})
        msg = jwt.encode({'msg': msg})
    return make_response('test failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/BillingHistory', methods=['GET', 'POST'])
def get_post(post_billing):
    billing_data = get_post
    msg = {}
    cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
    post = cur.execute('SELECT * FROM billing_histories WHERE id = ?',
                       (post_billing,)).fetchall()
    conn.close()
    if post is None:
        msg['billing_histories'] = 'No billing history'

        token = jwt.encode({'billing_data': id, 'exp': datetime.datetime})
        msg = jwt.encode({'billing_histories': msg})
        return jsonify({'token': token})
    return jsonify({'msg': msg})


@app.route('/', methods=['GET', 'POST'])
def download():
    p = 'file'
    if request.method == 'POST':
        p = request.form['p']
        send_file(p, as_attachment=True)
        token = jwt.encode({'user': p.file})
        return jsonify({'token': token})
    return make_response({'download': 'Basic realm'})


if __name__ == '__main__':
    app.run()
