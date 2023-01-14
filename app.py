from flask import Flask
from auth.register import get_started
from views.billingHistory import billing_history
from views.edit_email import change_email
from views.edit_password import change_password
from views.update_profile import change_profile_image
from views.logout import logout
from views.subscription import subscription
from views.TestOverview import overview
from auth.login import sign_in
from flask_cors import CORS
from flask_session import Session
from views.payments import payments
from flask_jwt_extended import (
    JWTManager, create_access_token
)


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'  # change this to a secure key
jwt = JWTManager(app)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app)
# app.app_context()
# app.secret_key = 'your secret key here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///config/TestLoad.sqlite'


app.register_blueprint(get_started)
app.register_blueprint(sign_in)
app.register_blueprint(billing_history)
app.register_blueprint(change_email)
app.register_blueprint(change_password)
app.register_blueprint(change_profile_image)
app.register_blueprint(logout)
app.register_blueprint(subscription)
app.register_blueprint(overview)
app.register_blueprint(payments)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
