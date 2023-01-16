from flask import request, jsonify
from flask_jwt_extended import jwt_required, unset_jwt_cookies

logout = Blueprint('logout', __name__)


@logout.route('/logout', methods=['POST'])
@jwt_required
def logout_user():
    unset_jwt_cookies(request, response)
    return jsonify({'success': True})
