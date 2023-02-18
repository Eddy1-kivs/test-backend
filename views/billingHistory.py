from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from flask import send_file
from fpdf import FPDF
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


billing_history = Blueprint('billing_history', __name__)


@billing_history.route('/billing-history-view', methods=['POST'])
@jwt_required()
def user_billing_history():
    user_id = get_jwt_identity()

    billing_history = session.query(BillingHistory.id, BillingHistory.username, BillingHistory.date,
                                    BillingHistory.details, BillingHistory.amount, BillingHistory.download)\
        .filter_by(id=user_id).all()
    if not billing_history:
        return []
    billing_history_list = []
    for billing in billing_history:
        billing_dict = {
            'id': billing.id,
            'username': billing.username,
            'date': billing.date,
            'details': billing.details,
            'amount': billing.amount,
            'download': billing.download
        }
        billing_history_list.append(billing_dict)
    return jsonify(billing_history_list)


@billing_history.route('/download-invoice-pdf', methods=['GET'])
@jwt_required()
def download_invoice():
    user_id = get_jwt_identity()
    invoice_id = request.args.get('invoice_id')

    if not invoice_id:
        return jsonify({'error': 'Missing invoice_id'}), 400

    billing_history = session.query(BillingHistory.id, BillingHistory.username, BillingHistory.date,
                                    BillingHistory.details,
                                    BillingHistory.amount).filter_by(user_id=user_id, id=invoice_id).first()

    if not billing_history:
        return jsonify({'error': 'Invalid invoice_id'}), 401

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Your Billing history", ln=0, align="C")
    pdf.cell(200, 10, txt="Billing ID: " + str(billing_history.id), ln=0, align="L")
    pdf.cell(200, 10, txt="Username: " + billing_history.username, ln=0, align="L")
    pdf.cell(200, 10, txt="Date: " + str(billing_history.date), ln=0, align="L")
    pdf.cell(200, 10, txt="Details: " + billing_history.details, ln=0, align="L")
    pdf.cell(200, 10, txt="Amount: " + str(billing_history.amount), ln=0, align="L")
    pdf.output("billing_history.pdf")
    try:
        return send_file("billing_history.pdf", as_attachment=True)
    except:
        return jsonify({'error': 'Error in sending invoice file'}), 500
