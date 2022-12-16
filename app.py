from flask import Flask
import sqlite3
from login import login
from register import register

app = Flask(__name__)
app.register_blueprint(register)
app.register_blueprint(login)


conn = sqlite3.connect('TestLoad.sqlite')
conn.close()

SECRET_KEY = 'my_secret_Key'

DATABASE = 'TestLoad.sqlite'


if __name__ == '__main__':
    app.run()
