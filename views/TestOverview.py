from flask import Flask, jsonify, Blueprint, json
from config.database import db


overview = Blueprint('overview', __name__)


@overview.route('/test-overview', methods=['GET', 'POST'])
def test():
    test_data = test
    msg = {}
    cur = db.connection.cursor(db.cursors.DictCursor)
    post = cur.execute('SELECT * FROM tests WHERE id = ?',
                       (test_data,)).fetchall()
    cur.close()
    if post is None:
        msg['billing_histories'] = 'No billing history'
        test_data = json.encode({'test': id})
        msg = json.encode({'msg': msg})
    return make_response('test failed', 401, {'www.Authenticate': 'Basic realm'})


