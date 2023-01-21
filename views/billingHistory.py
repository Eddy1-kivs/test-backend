from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from flask import send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from sqlalchemy.orm import scoped_session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

# Connect to the database
engine = create_engine('sqlite:///TestLoad.db', echo=True, poolclass=QueuePool, pool_size=5, max_overflow=10)
Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))
session.close()


# Create the User and Tests classes
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    location = Column(String)
    img = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)


class BillingHistory(Base):
    __tablename__ = 'billing_histories'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    username = Column(String)
    date = Column(Date)
    details = Column(String)
    amount = Column(Float)
    download = Column(String)
    user = relationship("User", backref="billing_histories")


# Base.metadata.create_all(engine)
billing_history = Blueprint('billing_history', __name__)


@billing_history.route('/billing-history-view', methods=['POST'])
@jwt_required()
def user_billing_history():
    user_id = get_jwt_identity()

    billing_history = session.query(BillingHistory.id, BillingHistory.username, BillingHistory.date,
                                    BillingHistory.details, BillingHistory.amount, BillingHistory.download)\
        .filter_by(id=user_id).all()
    if not billing_history:
        return jsonify({'billing': 'No billings found for this user.'})
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

    billing_history = session.query(BillingHistory).filter_by(user_id=user_id, id=invoice_id).first()
    if not billing_history:
        return jsonify({'error': 'Invalid invoice_id'}), 401

    try:
        invoice_file = billing_history.download
        os.path.exists(invoice_file)
        return send_file(invoice_file)
    except:
        return jsonify({'error': 'Error in sending invoice file'}), 500
