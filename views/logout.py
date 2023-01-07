import sqlite3
from flask import Blueprint, request, jsonify
from auth.login import session

logout = Blueprint('logout', __name__)


@logout.route('/logout', methods=['POST'])
def logout_user():
    # Clear the user's session data
    session.clear()

    return jsonify({'success': True})
