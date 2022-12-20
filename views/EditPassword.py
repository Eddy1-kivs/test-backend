from flask import Flask, request, jsonify, session, Blueprint

password_change = Blueprint('password_change', __name__)


@password_change.route('/EditEmailModal', methods=['GET', 'POST'])
def change_password(password_change_now):
    password = request.form
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        cur = db.connection.cursor(db.cursors.DictCursor)
        db.execute('UPDATE users SET email = %s  WHERE email = %s', email)
        db.commit()
        flash('Your email address has been updated successfully')
        token = jwt.encode({'user': email.email})
        return jsonify({'token': token})
    return make_response('email update failed', 401, {'www.Authenticate': 'Basic realm'})

