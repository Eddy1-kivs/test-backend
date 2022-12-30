from flask import Flask
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from auth.register import get_started
from views.billingHistory import billing
from views.download import download_file
from views.EditEmail import email_edit
from views.EditPassword import password_change
from views.EditProfilePicture import profile_edit
from views.logout import out
from views.add_payments import pay
from views.subscription import subs
from views.TestOverview import overview
from auth.login import sign_in
from views.payments import payments

load_dotenv()

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)
app.config['SECRET_KEY'] = 'hello'
url = os.getenv('DATABASE_URL')

# connection = psycopg2.connect(url)

app.register_blueprint(get_started)
app.register_blueprint(sign_in)
# app.register_blueprint(billing)
# app.register_blueprint(download_file)
# app.register_blueprint(email_edit)
# app.register_blueprint(password_change)
# app.register_blueprint(profile_edit)
# app.register_blueprint(out)
# app.register_blueprint(pay)
# app.register_blueprint(subs)
# app.register_blueprint(overview)
# app.register_blueprint(payments)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)