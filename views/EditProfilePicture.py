from flask import Flask, request, jsonify, session, Blueprint

profile_edit = Blueprint('profile_edit', __name__)


@profile_edit.route('/EditProfilePicture', methods=['GET', 'POST'])
def change_profile(profile_change):
    img = request.form
    if request.method == 'POST':
        img = request.form[bytes('profile')]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        DATABASE.execute(
            'UPDATE users SET username = %s, first_name = %s, last_name = %s, phone_number = %s  WHERE username = ?')
        DATABASE.commit()
        flash('Your profile has been updated successfully')
        token = jwt.encode({'user': profile_change['username', 'first_name', 'last_name', 'phone_number']})
        return jsonify({'token': token})
    return make_response('profile update failed', 401, {'www.Authenticate': 'Basic realm'})


