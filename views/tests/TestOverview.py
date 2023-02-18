from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from models import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


overview = Blueprint('overview', __name__)


@overview.route('/test-overview', methods=['POST'])
@jwt_required()
def test_overview():
    user_id = get_jwt_identity()
    user_tests = session.query(Tests.id, Tests.test_url, Tests.start_date, Tests.total_runs, Tests.last_run).filter_by(id=user_id).all()
    if not user_tests:
        return []
    user_tests_list = []
    for test in user_tests:
        test_dict = {
            'id': test.id,
            'test_url': test.test_url,
            'start_date': test.start_date,
            'total_runs': test.total_runs,
            'last_run': test.last_run,
        }
        user_tests_list.append(test_dict)
    return jsonify(user_tests_list)


@overview.route('/delete-test', methods=['POST'])
@jwt_required()
def delete_test():
    user_id = get_jwt_identity()
    test_id = request.args.get('id')
    if not test_id:
        return jsonify({'error': 'Missing test_id'}), 400

    test = session.query(Tests).filter_by(user_id=user_id, id=test_id).first()
    if not test:
        return jsonify({'error': 'Invalid test_id'}), 401

    try:
        session.delete(test)
        session.commit()
        return jsonify({'message': 'Test deleted successfully'}), 200
    except:
        return jsonify({'error': 'Error in deleting test'}), 500



