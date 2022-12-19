from flask import Flask, request, jsonify, session, Blueprint


app = Flask(__name__)
sign_in = Blueprint('sign_in', __name__)


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


app.run(debug=True, host='0.0.0.0', port=8000)