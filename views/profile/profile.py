from flask import request, jsonify, Blueprint,  Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from config import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


user_profile = Blueprint('user_profile', __name__)


def to_dict(obj):
    """Convert SQLAlchemy object to dictionary"""
    d = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        d[column.name] = value
    return d


@user_profile.route('/profile', methods=['POST'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user_profile = session.query(User).filter_by(id=user_id).all()
    if not user_profile:
        return jsonify({'profile': 'profile is not updated'})
    profile_list = [{k: v for k, v in to_dict(prof).items() if k not in ['password', 'created_at', 'updated_at']} for
                    prof in user_profile]
    session.close()
    return jsonify({'profile': profile_list})

