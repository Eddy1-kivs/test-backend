import sqlite3
from flask import Blueprint, jsonify
from auth.login import session

overview = Blueprint('overview', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@overview.route('/test-overview', methods=['GET'])
def test():
    user_id = session['user_id']

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
