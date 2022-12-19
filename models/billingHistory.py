from flask import Flask, request, jsonify, session, Blueprint

app = Flask(__name__)
billing = Blueprint('billing', __name__)


@app.route('/BillingHistory', methods=['GET', 'POST'])
def get_post(post_billing):
    billing_data = get_post
    msg = {}
    cur = db.connection.cursor(db.cursors.DictCursor)
    post = cur.execute('SELECT * FROM billing_histories WHERE id = ?',
                       (post_billing,)).fetchall()
    cur.close()
    if post is None:
        msg['billing_histories'] = 'No billing history'

        token = jwt.encode({'billing_data': id, 'exp': datetime.datetime})
        msg = jwt.encode({'billing_histories': msg})
        return jsonify({'token': token})
    return jsonify({'msg': msg})


app.run(debug=True, host='0.0.0.0', port=8000)