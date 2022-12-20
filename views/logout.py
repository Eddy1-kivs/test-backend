from flask import Flask, request, jsonify, session, Blueprint

out = Blueprint('out', __name__)


@out.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user_name', None)
    return 'logged out successfully'

