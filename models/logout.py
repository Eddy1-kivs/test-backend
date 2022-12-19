from flask import Flask, request, jsonify, session, Blueprint

app = Flask(__name__)
out = Blueprint('out', __name__)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user_name', None)
    return 'logged out successfully'


app.run(debug=True, host='0.0.0.0', port=8000)