from flask import Flask, request, Blueprint, jsonify

app = Flask(__name__)
login = Blueprint('login',
                  __name__,
                  url_prefix='login')


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


@app.route('/', methods=['GET', 'POST'])
def sign_in():
    auth = request.form
    login_error = {}
    if auth == 'POST' and 'user_name' in request.form and 'password' in request.form:
        user_name = request.form[StringField('username')]
        password = request.form[StringField('password')]
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
        return jsonify({'logged in': auth})
    return jsonify({'login_error': login_error})
