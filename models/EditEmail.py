from flask import Flask, request, jsonify, session, Blueprint

app = Flask(__name__)
email_edit = Blueprint('email_edit', __name__)


@app.route('/EditEmailModal', methods=['GET', 'POST'])
def change_email(email_change):
    email = request.form
    if request.method == 'POST':
        email = request.form[StringField('Email')]
        cur = db.connection.cursor(DATABASE.cursors.DictCursor)
        db.execute('UPDATE users SET email = %s  WHERE email = %s', email)
        db.commit()
        flash('Your email address has been updated successfully')
        token = jwt.encode({'user': email.email})
        return jsonify({'token': token})
    return make_response('email update failed', 401, {'www.Authenticate': 'Basic realm'})


app.run(debug=True, host='0.0.0.0', port=8000)