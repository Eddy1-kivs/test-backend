import datetime
import re
from functools import wraps
import jwt as jwt
from flask import Flask, request, jsonify, flash, make_response, session, send_file
import sqlite3
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)


conn = sqlite3.connect('TestLoad.sqlite')
conn.close()

SECRET_KEY = 'secretKey'

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
    if auth == 'POST' and 'first_name' in request.form \
            and 'user_name' in request.form and 'password' in \
            request.form and 'email' in request.form:
        first_name = request.form[str('first_name',)]
        last_name = request.form[str('last_name',)]
        phone_number = request.form[str('phone_number')]
        username = request.form[str('username')]
        email = request.form[str('email')]
        password = request.form[str('password')]
        created_at = request.form[str('created_at')]
        updated_at = request.form[str('updated_at')]
        img = request.form[bytes('img')]
        location = request.form[str('location')]

        cur = DATABASE.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (username, password))
        user = cur.fetchone()

        if user:
            flash('Account already exists')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            cur = conn.cursor()
            cur.execute("INSERT INTO users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (first_name, last_name,
                            phone_number, username,
                            email, password, created_at,
                            updated_at, img, location))

            DATABASE.commit()
            flash('You have successfully registered!')
            token = jwt.encode({'user': auth.user_name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=
                                                                                                               30)})
            return jsonify({'token': token})
    return make_response('Registration failed', 401, {'www.Authenticate': 'Basic realm="registration required"'})

# Login page
# the user will fill the form with their credentials
# if the credentials are valid, the user will be logged in and redirected to home page
# if the credentials are invalid, the user will not be logged in.
# they will be required to fill out the login form again with valid credentials
#


@app.route('/', methods=['GET', 'POST'])
def login():
    auth = request.form
    if auth == 'POST' and 'user_name' in request.form and 'password' in request.form:
        user_name = request.form['username']
        password = request.form['password']
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('SELECT * FROM users WHERE users.username =%s AND password = %s', (user_name, password))
        user = cur.fetchone()
        if not user:
            flash('Invalid username or password')
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['user_name'] = user['user_name']
            return 'logged in successfully'
        else:
            flash('incorrect username/password')
            token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)})
            return jsonify({'token': token})
    return make_response('log in failed', 401, {'www.Authenticate': 'Basic realm="login required"'})


@app.route('/', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user_name', None)
    return 'logged out successfully'


@app.route('/', methods=['GET', 'POST'])
def change_email(email_change):
    email = StringField('Email', validators=[DataRequired()])
    if request.method == 'POST':
        email_change['email'] = email.data
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('UPDATE users SET email = %s  WHERE email = %s', email)
        DATABASE.commit()
        flash('Your email address has been updated successfully')
        token = jwt.encode({'user': email.email})
        return jsonify({'token': token})
    return make_response('email update failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/', methods=['GET', 'POST'])
def change_password(password_change):
    password = StringField('password', validators=[DataRequired()])
    if request.method == 'POST':
        password_change['password'] = password.data
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('UPDATE users SET password = %s WHERE password = %s', password)
        DATABASE.commit()
        flash('Your password has been updated successfully')
        token = jwt.encode({'user': password.password})
        return jsonify({'token': token})
    return make_response('password update failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/', methods=['GET', 'POST'])
def change_profile(profile_change):
    username = StringField('profile', validators=[DataRequired()])
    first_name = StringField('first name', validators=[DataRequired()])
    last_name = StringField('last name', validators=[DataRequired()])
    phone_number = StringField('phone number', validators=[DataRequired()])
    if request.method == 'POST':
        profile_change['username'] = username.data
        profile_change['first_name'] = first_name.data
        profile_change['last_name'] = last_name.data
        profile_change['phone_number'] = phone_number.data
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('UPDATE users SET username = %s, first_name = %s, last_name = %s, phone_number = %s  WHERE username = ?')
        DATABASE.commit()
        flash('Your profile has been updated successfully')
        token = jwt.encode({'user': profile_change['username', 'first_name', 'last_name', 'phone_number']})
        return jsonify({'token': token})
    return make_response('profile update failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/', methods=['GET', 'POST'])
def subscription():
    subscribe = request.form
    if subscribe == 'POST' and 'username' in request.form and 'current_plan' in request.form and 'plan_amount' in request.form and 'card_number' in request.form and 'created_at' in request.form:
        username = request.form['username']
        current_plan = request.form['current_plan']
        plan_amount = request.form['plan_amount']
        card_number = request.form['card_number']
        created_at = request.form['created_at']
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


@app.route('/', methods=['GET', 'POST'])
def add_payment():
    add = request.form
    if add == 'POST' and 'username' in request.form and 'card_number' in request.form and 'card_holder_name' in request.form and 'expiration_date' in request.form and 'cvv' in request.form:
        username = request.form['username']
        card_number = request.form['card_number']
        card_holder_name = request.form['card_holder_name']
        expiration_date = request.form['expiration_date']
        cvv = request.form['cvv']
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


@app.route('/', methods=['GET', 'POST'])
def test():
    test_data = request.form
    if test_data == 'POST' and 'username' in request.form and 'location' in request.form and 'browser' in request.form and 'test_url' in request.form and 'results' in request.form:
        username = request.form['username']
        location = request.form['location']
        browser = request.form['browser']
        test_url = request.form['test_url']
        results = request.form['results']
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        cur.execute("INSERT INTO tests VALUES (%s,%s,%s,%s,%s,%s)",
                    (username,
                     location,
                     browser,
                     test_url,
                     results))
        DATABASE.commit()
        flash('Your test has been stored!')
        token = jwt.encode({'tests': username, 'exp': datetime.datetime.utcnow()})
        return jsonify({'token': token})
    return make_response('test failed', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/', methods=['GET', 'POST'])
def billing_histories():
    billing = request.form
    if billing == 'POST' and 'username' in request.form and 'date' in request.form and 'details' in request.form and 'amount' in request.form and 'download' in request.form:
        username = request.form['username']
        date = request.form['date']
        details = request.form['details']
        amount = request.form['amount']
        download_file = request.form['download']
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        cur.execute("INSERT INTO billing_histories VALUES (%s,%s,%s,%s,%s,%s)",
                    (username,
                     date,
                     details,
                     amount,
                     download_file))
        DATABASE.commit()
        flash('Your billing history has been stored!')
        token = jwt.encode({'billing_histories': username, 'exp': datetime.datetime})
        return jsonify({'token': token})
    return make_response('billing history failed to store', 401, {'www.Authenticate': 'Basic realm'})


@app.route('/', methods=['GET', 'POST'])
def download():
    p = 'file'
    if request.method == 'POST':
        p = request.form['p']
        send_file(p, as_attachment=True)
        token = jwt.encode({'user': p.file})
        return jsonify({'token': token})
    return make_response('file failed to download', 401, {'www.Authenticate': 'Basic realm'})


if __name__ == '__main__':
    app.run()
