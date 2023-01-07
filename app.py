from flask import Flask
from auth.register import get_started
from views.billingHistory import billing_history
from views.EditEmail import change_email
from views.EditPassword import change_password
from views.EditProfilePicture import change_profile_image
from views.logout import logout
from views.subscription import subscription
from views.TestOverview import overview
from auth.login import sign_in
from views.payments import payments
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context()
app.secret_key = 'your secret key here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TestLoad.sqlite'


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
    app.run(debug=True, host="0.0.0.0", port=5000)