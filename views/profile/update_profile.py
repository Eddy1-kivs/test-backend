import bcrypt
import re
import datetime
import os
import phonenumbers
import uuid
from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from models import *
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


update_profile = Blueprint('update_profile', __name__)


def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return False
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    return True


@update_profile.route('/edit-profile', methods=['POST'])
@jwt_required()
def update_user_profile():
    user_id = get_jwt_identity()

    errors = {}
    required_fields = ['first_name', 'last_name', 'phone_number']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 302

    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    location = request.get_json().get('location')
    phone_number = request.get_json().get('phone_number')
    if not validate_phone_number(phone_number):
        errors['phone_number'] = 'Invalid phone number'
    updated_at = datetime.now()

    if errors:
        return jsonify(errors), 302

    # update the user profile
    session.query(User).filter(User.id == user_id).update({
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'location': location,
        # 'img': img,
        'updated_at': updated_at
    })
    session.commit()
    return jsonify({'success': True})


