from flask import Flask
import sqlite3
from login import login
# from register import new

api = Flask(__name__)
# app.register_blueprint(new)
# app.register_blueprint(login)


conn = sqlite3.connect('TestLoad.sqlite')
conn.close()


SECRET_KEY = 'my_secret_Key'

db = 'TestLoad.sqlite'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
