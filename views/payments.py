import json
import sqlite3

from flask import Flask, jsonify, Blueprint
from config.database import db

payments = Blueprint('payments', __name__)


@payments.route('/')
@payments.route('/payments', methods=['GET'])
def get_payments():
    con = sqlite3.connect("/TestLoad.sqlite")
    cur.execute("SELECT * FROM main.payments  WHERE id = ?")
    data = cur.fetchall()
    cur.close()
    get_jti(payments)
    return jsonify({'payments': payments}), 200