from flask import Flask
import os
from dotenv import load_dotenv
from auth.register import get_started
from models.billingHistory import billing
from models.download import download_file
from models.EditEmail import email_edit
from models.EditPassword import password_change
from models.EditProfilePicture import profile_edit
from models.logout import out
from models.payment import pay
from models.subscription import subs
from models.TestOverview import overview
from auth.login import sign_in

load_dotenv()

app = Flask(__name__)
url = os.getenv('DATABASE_URL')
# connection = psycopg2.connect(url)
# app.register_blueprint(get_started)
app.register_blueprint(sign_in)
app.register_blueprint(billing)
app.register_blueprint(download_file)
app.register_blueprint(email_edit)
app.register_blueprint(password_change)
app.register_blueprint(profile_edit)
app.register_blueprint(out)
app.register_blueprint(pay)
app.register_blueprint(subs)
app.register_blueprint(overview)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
