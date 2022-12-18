from app import *


@app.route('/EditEmailModal', methods=['GET', 'POST'])
def change_email(email_change):
    email = request.form
    if request.method == 'POST':
        email = request.form[StringField('Email')]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute('UPDATE users SET email = %s  WHERE email = %s', email)
        DATABASE.commit()
        flash('Your email address has been updated successfully')
        token = jwt.encode({'user': email.email})
        return jsonify({'token': token})
    return make_response('email update failed', 401, {'www.Authenticate': 'Basic realm'})
