from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
@jwt_required()
def users():
    user = get_jwt_identity()
    if not user:
        return jsonify({"msg": "Invalid user"}), 302
    user = session.query(User.id, User.username, User.email, User.first_name, User.last_name, User.location,
                         User.phone_number, User.img).filter_by\
        (id=user).first()
    session.close()
    if not user:
        return jsonify({'user': 'user does not exist'}), 302
    user_dict = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'location': user.location,
        'phone_number': user.phone_number,
        'img': user.img,
    }
    return jsonify({'user': user_dict})
