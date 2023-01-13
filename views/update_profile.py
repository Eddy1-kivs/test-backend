import sqlite3
from flask import Blueprint, request, jsonify
from auth.login import session
import datetime

change_profile_image = Blueprint('change_profile_image', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@change_profile_image.route('/change-profile-image', methods=['POST'])
def change_profile_user_image():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized access'}), 401

    errors = {}
    required_fields = ['first_name', 'last_name', 'phone_number']
    for field in required_fields:
        if not request.get_json().get(field):
            errors[field] = 'This field is required'

    if errors:
        return jsonify(errors), 400

    image = request.files.get('image')
    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    phone_number = request.get_json().get('phone_number')
    location = request.get_json().get('location')
    updated_at = datetime.datetime.utcnow().isoformat()

    conn = get_db()
    cursor = conn.cursor()
    # Save the image to disk and retrieve the image file path
    image_file_path = save_image(image)

    cursor.execute('''
        UPDATE users SET img=? WHERE username=?
    ''', (image_file_path, first_name, last_name, phone_number, location, updated_at))
    conn.commit()

    return jsonify({'success': True})


def save_image(image):
    # Save the image to disk and return the file path
    # .
    return image_file_path