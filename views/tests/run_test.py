from flask import request, jsonify, Blueprint, Flask
from datetime import datetime
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
jwt = JWTManager(app)


run_test = Blueprint('run_test', __name__)


@run_test.route("/run_test", methods=["POST"])
@jwt_required()
def test_run():
    user_id = get_jwt_identity()
    return
