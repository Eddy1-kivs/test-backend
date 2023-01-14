import sqlite3
from flask import Blueprint, request, jsonify
from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies

logout = Blueprint('logout', __name__)


@logout.route('/logout', methods=['POST'])
def logout_user():
    user_id = get_jwt_identity()
    response = make_response(jsonify({'success': True}), 200)
    unset_jwt_cookies(response)
    return response