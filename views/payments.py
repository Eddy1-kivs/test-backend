import json
import sqlite3

from flask import Flask, jsonify, Blueprint
from config.database import db

payments = Blueprint('payments', __name__)


# @payments.route('/')
@payments.route('/payments', methods=['GET'])
def get_payments():
    con = db.cursor(db)
    cur = con.cursor()
    cur.execute('SELECT * FROM main.payments WHERE id = ?')
    users = cur.fetchone()
    get_jti(payments)
    return jsonify({'payments': payments}), 200