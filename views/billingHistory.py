import sqlite3
from flask import Blueprint, request, jsonify

billing_history = Blueprint('billing_history', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@billing_history.route('/billing-history', methods=['GET'])
def user_billing_history():
    username = request.args.get('username')
    password = request.args.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username '}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM billing_histories WHERE username=?
    ''', username)
    billing_history = cursor.fetchall()
    if not billing_history:
        return jsonify({'billing_history': 'No billing history found'})

    return jsonify({'billing_history': billing_history})


@billing_history.route('/download-invoice', methods=['GET'])
def download_invoice():
    username = request.args.get('username')
    password = request.args.get('password')
    invoice_id = request.args.get('invoice_id')

    if not username or not password or not invoice_id:
        return jsonify({'error': 'Missing username or invoice_id'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM billing_histories WHERE username=? AND id=?
    ''', (username, invoice_id))
    invoice = cursor.fetchone()
    if not invoice:
        return jsonify({'error': 'Invalid username or invoice_id'}), 401

    # Retrieve the invoice file from disk and send it to the user
    # ...

    return send_file(invoice_file)
