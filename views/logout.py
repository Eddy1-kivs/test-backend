from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import jwt_required, unset_jwt_cookies

logout = Blueprint('logout', __name__)


@logout.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    response = Response()
    unset_jwt_cookies(response)
    return jsonify({'success': True})
