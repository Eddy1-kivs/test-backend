from datetime import datetime, timedelta
from sqlalchemy.orm import scoped_session
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from sqlalchemy.orm import declarative_base

engine = create_engine('sqlite:///TestLoad.db', poolclass=QueuePool, pool_size=10, max_overflow=20)
Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))
session.close()

# echo=true


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
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


class Subscriptions(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    current_plan = Column(String)
    plan_amount = Column(Float)
    card_number = Column(String)
    created_at = Column(Date)
    user = relationship("User", backref="subscriptions")


# class Payments(Base):
#     __tablename__ = 'payments'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     username = Column(String)
#     card_number = Column(String)
#     card_holder_name = Column(String)
#     expiration_date = Column(Date)
#     cvv = Column(String)
#     created_at = Column(Date)
#     user = relationship("Subscriptions", backref="payments")

class Tests(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    username = Column(String)
    location = Column(String)
    browser = Column(String)
    test_url = Column(String)
    results = Column(String)
    start_date = Column(String)
    total_runs = Column(Integer)
    last_run = Column(String)
    user = relationship("User", backref="tests")


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


Base.metadata.create_all(engine)

