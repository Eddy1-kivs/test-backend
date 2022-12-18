from app import *


@app.route('/test-overview', methods=['GET', 'POST'])
def test():
    test_data = test
    msg = {}
    cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
    post = cur.execute('SELECT * FROM tests WHERE id = ?',
                       (test_data,)).fetchall()
    conn.close()
    if post is None:
        msg['billing_histories'] = 'No billing history'
        test_data = jwt.encode({'test': id})
        msg = jwt.encode({'msg': msg})
    return make_response('test failed', 401, {'www.Authenticate': 'Basic realm'})
