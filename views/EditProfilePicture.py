import sqlite3
from flask import Blueprint, request, jsonify

change_profile_image = Blueprint('change_profile_image', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@change_profile_image.route('/change-profile-image', methods=['POST'])
def change_profile_user_image():
    username = request.form.get('username')
    password = request.form.get('password')
    image = request.files.get('image')

    if not username or not password or not image:
        return jsonify({'error': 'Missing username, password, or image'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username=? AND password=?
    ''', (username, password))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Save the image to disk and retrieve the image file path
    image_file_path = save_image(image)

    cursor.execute('''
        UPDATE users SET img=? WHERE username=?
    ''', (image_file_path, username))
    conn.commit()

    return jsonify({'success': True})


def save_image(image):
    # Save the image to disk and return the file path
    # ...
    return image_file_path