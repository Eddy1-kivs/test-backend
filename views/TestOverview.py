import sqlite3
from flask import Blueprint, request, jsonify

overview = Blueprint('overview', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@overview.route('/test-overview', methods=['GET'])
def test():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM tests
        WHERE username=? AND location=? AND browser AND test_url AND results
    ''', (username, password))
    tests = cursor.fetchall()
    if not tests:
        return jsonify({'tests': 'No test'})

    return jsonify({'tests': tests})


