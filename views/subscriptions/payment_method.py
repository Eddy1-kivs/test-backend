from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import scoped_session
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

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


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_number = Column(String)
    card_holder_name = Column(String)
    expiration_date = Column(String)
    cvv = Column(String)
    created_at = Column(String)
    user = relationship("User", backref="payments")

    # Base.metadata.create_all(engine)


payment_methods = Blueprint('payment_methods', __name__)


@payment_methods.route('/payment_methods', methods=['POST'])
@jwt_required()
def payment_queries():
    user_id = get_jwt_identity()
    payments = session.query(Payments.id, Payments.card_number, Payments.card_holder_name, Payments.expiration_date,
                             Payments.cvv, Payments.created_at).filter_by(user_id=user_id).all()
    if not payments:
        return jsonify({'tests': 'No payment methods found for this user.'})
    user_payment_methods = []
    for payment in payments:
        payment_dict = {
            'id': payment.id,
            'card_number': payment.card_number,
            'card_holder_name': payment.card_holder_name,
            'expiration_date': payment.expiration_date,
            'cvv': payment.cvv,
            'created_at': payment.created_at,
        }
        user_payment_methods.append(payment_dict)
    return jsonify({'user_payments': user_payment_methods})


@payment_methods.route('/delete-payment-method', methods=['DELETE'])
@jwt_required()
def delete_payment_method():
    user_id = get_jwt_identity()
    payment_id = request.args.get('payment_id')
    if not payment_id:
        return jsonify({'error': 'Missing payment_id'}), 400
    payment = session.query(Payments).filter_by(user_id=user_id, id=payment_id).first()
    if not payment:
        return jsonify({'error': 'Invalid payment_id'}), 401
    session.delete(payment)
    session.commit()
    return jsonify({'message': 'Payment method deleted successfully.'}), 200
