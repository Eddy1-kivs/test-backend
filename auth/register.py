from flask import Flask, request, jsonify, session, Blueprint
from config.database import db


get_started = Blueprint('get_started', __name__)


@get_started.route('/')
@get_started.route('/register', methods =['GET', 'POST'])
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