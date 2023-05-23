import os
import logging
import base64
from flask import request, jsonify, Blueprint
import requests
import webbrowser
import datetime
import json
from models import *
from flask_jwt_extended import jwt_required, get_jwt_identity

run_test = Blueprint('run_test', __name__)

logger = logging.getLogger(__name__)


def test_url(url):
    try:
        response = requests.get(url, timeout=5)
        return {
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            # "content": base64.b64encode(response.content).decode()
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making request to URL: {e}")
        return {"error": "Error making request to URL"}
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout error: {e}")
        return {"error": "Timeout error"}
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        return {"error": "Connection error"}


@run_test.route("/test", methods=["POST"])
@jwt_required()
def test():
    user_id = get_jwt_identity()
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "Please provide a URL to test"}), 400

    start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = test_url(url)

    user_agent = request.headers.get('User-Agent')
    logger.info(f"User-Agent: {user_agent}")
    browser = "Unknown browser"

    if "Chrome" in user_agent:
        browser = "Google Chrome"
    elif "Firefox" in user_agent:
        browser = "Mozilla Firefox"
    elif "Safari" in user_agent:
        browser = "Apple Safari"
    elif "MSIE" in user_agent or "Trident" in user_agent:
        browser = "Internet Explorer"
    elif "Opera" in user_agent:
        browser = "Opera"

    if request.headers.get("User-Agent").startswith("Mozilla") and request.headers.get("Referer") != "":
        user_location = {"error": "Geolocation API is not supported in this browser."}
    else:
        try:
            user_location = requests.get("http://ip-api.com/json").json()
        except Exception as e:
            user_location = {"error": f"Error getting user location: {e}"}
    location = user_location
    # results["user_location"] = user_location
    browsers = browser
    # results["browser"] = browser

    user_id = get_jwt_identity()
    user = session.query(User).filter_by(id=user_id).first()

    # Check if the URL has already been tested
    existing_test = session.query(Tests).filter_by(user_id=user.id, test_url=url).first()

    browser_str = json.dumps(browser)
    if existing_test:
        # Update the existing test
        location_str = json.dumps(user_location)
        results_str = json.dumps(results)
        existing_test.location = location_str
        # existing_test.browser = ["browser"]3#
        existing_test.results = results_str
        existing_test.total_runs += 1
        existing_test.last_run = start_date
    else:
        location_str = json.dumps(user_location)
        results_str = json.dumps(results)

        # If the URL has not been tested, create a new test
        new_test = Tests(
            user_id=user.id,
            username=user.username,
            location=location_str,
            browser=browser_str,
            test_url=url,
            results=results_str,
            start_date=start_date,
            total_runs=1,
            last_run=start_date
        )
        session.add(new_test)

    session.commit()

    return jsonify(results, location, browsers)
