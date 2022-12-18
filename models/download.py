from app import *


@app.route('/', methods=['GET', 'POST'])
def download():
    p = 'file'
    if request.method == 'POST':
        p = request.form['p']
        send_file(p, as_attachment=True)
        token = jwt.encode({'user': p.file})
        return jsonify({'token': token})
    return make_response({'download': 'Basic realm'})
