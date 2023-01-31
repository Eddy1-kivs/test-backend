import bcrypt
import re
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


change_email = Blueprint('change_email', __name__)


@change_email.route('/email-change', methods=['POST'])
@jwt_required()
def change_your_email():
    user_id = get_jwt_identity()

    errors = {}
    required_fields = ['current_email', 'new_email_address', 'confirm_email', 'password']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 302

    current_email = request.get_json().get('current_email')
    new_email_address = request.get_json().get('new_email_address')
    confirm_email = request.get_json().get('confirm_email')
    password = request.get_json().get('password')

    if new_email_address != confirm_email:
        errors['confirm_email'] = 'New email address and confirm email address do not match'
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email_address):
        errors['new_email_address'] = 'Invalid email format'
    if new_email_address == current_email:
        errors['new_email_address'] = 'New email address is the same as current email'

    if errors:
        return jsonify(errors), 302

    user = session.query(User).filter_by(id=user_id).one()
    if not user:
        errors['current_email'] = 'Invalid email'

    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        errors['password'] = 'Invalid password'

    if errors:
        return jsonify(errors), 302

    existing_user = session.query(User).filter_by(email=new_email_address).first()
    if existing_user:
        errors['new_email_address'] = 'This email address is already in use'
        return jsonify(errors), 302

    user.email = new_email_address
    session.commit()
    session.close()

    return jsonify({'success': True})
