from flask import Flask, request, jsonify, session, Blueprint

app = Flask(__name__)
download_file = Blueprint('download_file', __name__)


@app.route('/', methods=['GET', 'POST'])
def download():
    p = 'file'
    if request.method == 'POST':
        p = request.form['p']
        send_file(p, as_attachment=True)
        token = jwt.encode({'user': p.file})
        return jsonify({'token': token})
    return make_response({'download': 'Basic realm'})


app.run(debug=True, host='0.0.0.0', port=8000)