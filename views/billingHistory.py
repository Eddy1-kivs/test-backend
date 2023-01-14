import sqlite3
from flask import Blueprint, request, jsonify, send_file, session

billing_history = Blueprint('billing_history', __name__)


def get_db():
    conn = sqlite3.connect('config/TestLoad.sqlite')
    return conn


@billing_history.route('/billing-history-view', methods=['GET'])
def user_billing_history():
    user_id = session['user_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
            SELECT * FROM billing_histories WHERE id=?
        ''', (user_id,))
    billing_history = cursor.fetchall()
    if not billing_history:
        return jsonify({'billing_history': 'No billing history found'})

    return jsonify({'billing_history': billing_history})


@billing_history.route('/download-invoice-pdf', methods=['GET'])
def download_invoice(invoice_file=None):
    user_id = get_jwt_identity()
    invoice_id = request.args.get('invoice_id')

    if not invoice_id:
        return jsonify({'error': 'Missing invoice_id'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM billing_histories WHERE user_id=? AND invoice_id=?
    ''', (user_id, invoice_id))
    invoice = cursor.fetchone()
    if not invoice:
        return jsonify({'error': 'Invalid invoice_id'}), 401

    # Retrieve the invoice file from disk and send it to the user
    try:
        invoice_file = invoice[4]
        return send_file(invoice_file)
    except:
        return jsonify({'error': 'Error in sending invoice file'}), 500
