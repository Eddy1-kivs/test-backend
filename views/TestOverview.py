import sqlite3
from flask import Blueprint, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity


overview = Blueprint('overview', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@overview.route('/test-overview', methods=['GET'])
def test():
    user_id = get_jwt_identity()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tests
        WHERE id=?
    ''', (user_id,))
    tests = cursor.fetchall()
    if not tests:
        return jsonify({'tests': 'No test'})

    return jsonify({'tests': tests})
