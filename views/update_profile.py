import sqlite3
import uuid
from flask import Blueprint, request, jsonify, session
import datetime
import os

update_profile = Blueprint('update_profile', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@update_profile.route('/profile_update', methods=['POST'])
def change_profile_user_image():
    user_id = session['user_id']

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
        UPDATE users SET img=?, first_name=?, last_name=?, phone_number=?, location=?, updated_at=? WHERE user_id=?
    ''', (image_file_path, first_name, last_name, phone_number, location, updated_at, user_id))
    conn.commit()

    return jsonify({'success': True})


def save_image(image):
    if not image:
        return None

    file_ext = os.path.splitext(image.filename)[1]
    file_name = f"{str(uuid.uuid4())}{file_ext}"
    file_path = os.path.join("path/to/save/images", file_name)

    image.save(file_path)
    return file_path