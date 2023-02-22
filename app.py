from flask import Flask
from auth.register import get_started
from views.billingHistory import billing_history
from views.settings.edit_email import change_email
from views.settings.edit_password import change_password
from views.profile.update_profile import update_profile
from views.logout import logout
from views.tests.TestOverview import overview
from auth.login import sign_in
from views.profile.user import user
from views.subscriptions.payments import payments
from views.subscriptions.add_subscritpion import add_subscription
from views.subscriptions.subscription import subscription
from views.profile.profile import user_profile
from views.profile.update_image import update_image
from views.tests.run_test import run_test
from views.subscriptions.payment_method import payment_methods
from flask_cors import CORS
from flask_session import Session
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)

app.register_blueprint(get_started)
app.register_blueprint(sign_in)
app.register_blueprint(billing_history)
app.register_blueprint(change_email)
app.register_blueprint(change_password)
app.register_blueprint(update_profile)
app.register_blueprint(logout)
app.register_blueprint(user)
app.register_blueprint(update_image)
app.register_blueprint(user_profile)
app.register_blueprint(subscription)
app.register_blueprint(add_subscription)
app.register_blueprint(overview)
app.register_blueprint(run_test)
app.register_blueprint(payments)
app.register_blueprint(payment_methods)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
