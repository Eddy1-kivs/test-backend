from app import *


@app.route('/BillingHistory', methods=['GET', 'POST'])
def get_post(post_billing):
    billing_data = get_post
    msg = {}
    cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
    post = cur.execute('SELECT * FROM billing_histories WHERE id = ?',
                       (post_billing,)).fetchall()
    conn.close()
    if post is None:
        msg['billing_histories'] = 'No billing history'

        token = jwt.encode({'billing_data': id, 'exp': datetime.datetime})
        msg = jwt.encode({'billing_histories': msg})
        return jsonify({'token': token})
    return jsonify({'msg': msg})
