import re
import os
from flask import send_from_directory
import uuid
from flask import request, jsonify, Blueprint,  Flask, render_template
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


update_image = Blueprint('update_image', __name__)


def save_image(image):
    if not image:
        return None
    try:
        file_ext = os.path.splitext(image.filename)[1]
        file_name = f"{str(uuid.uuid4())}{file_ext}"
        file_path = os.path.join("images/profile_images/", file_name)
        image.save(file_path)
    except:
        return None
    return file_path


@update_image.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)


@update_image.route('/edit-image', methods=['POST'])
@jwt_required()
def update_user_image():
    user_id = get_jwt_identity()
    errors = {}
    required_fields = ['img']
    for field in required_fields:
        if not request.files.get(field):
            errors[field] = 'image is required'

    if errors:
        return jsonify(errors), 302

    img = request.files.get('img')

    image_file_path = save_image(img)

    session.query(User).filter(User.id == user_id).update({
        'img': image_file_path,
    })
    session.commit()
    return jsonify({'success': True, 'file_path': image_file_path})

