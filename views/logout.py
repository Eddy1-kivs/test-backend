from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,
    create_refresh_token, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,
    get_jti
)
from datetime import datetime, timedelta

logout = Blueprint('logout', __name__)

blacklisted_jti = set()


@logout.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    jti = get_jwt_identity()
    blacklisted_jti.add(jti)
    expires = datetime.utcnow() - timedelta(seconds=1)
    response = jsonify({"msg": "Successfully logged out"})
    response.set_cookie("access_token_cookie", expires=expires)
    response.set_cookie("refresh_token_cookie", expires=expires)
    return response, 200

