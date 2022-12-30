import os
# import psycopg2
from dotenv import load_dotenv
from flask import Flask
import sqlite3

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'
url = os.getenv('DATABASE_URL')
# connection = psycopg2.connect(url)

conn = sqlite3.connect('TestLoad.sqlite')
conn.close()

db = 'TestLoad.sqlite'


# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()