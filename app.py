#!/usr/bin/python3
"""
the main module of the app
"""
from backend_code.database.data_operations import close_session, get_data_with_email, get_emails_data, insert_data
from backend_code.database.user_operations import get_user_data_email_username, update_user_data_id
from backend_code.word_fliter import words_filter
from flask import Flask, make_response, jsonify, request, render_template, make_response
from flask_cors import CORS
import re
import base64
from validate import validate
from jwt_encoding_decoding_method import verify_jwt
from backend_code import app_views



app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(app_views)


@app.route("/spam_filter/check", strict_slashes=False, methods=['GET'])
def filter_content():
    """ filter the content and decide if the email is spam or ham """
    print(request.cookies)
    jwt_token = request.cookies.get('token')
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({'state': 'not authenticated'}), 401

    user_id = data['data_1']
    content = request.args.get("content")
    email = request.args.get("email")

    if email != "" and content != "":
        content = base64.b64decode(content).decode('utf-8')
        email = base64.b64decode(email).decode('utf-8')
        valid = validate(email, content)
        if (valid != "okay"):
            return jsonify({"state": valid})

        result, ham, spam = words_filter(content, email)

        if result != "Spam Email":
            output = get_data_with_email(user_id, email)
            if output is not None:
                result = "Spam Email"

        return jsonify({"state": result, "spam": spam, "ham": ham})
    else:
        return jsonify({"state": "please fill all fields"})


@app.route("/spam_filter/add_email", strict_slashes=False, methods=['POST'])
def add_email():
    """ add email in case the user doesn't expect to get emails from this email address"""
    email = request.json["email"]
    pattern = r"[\w-]{5,}(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}"
    result = re.match(pattern, email)

    if email is not None and result:
        insert_data(email)
    else:
        return jsonify({"state": "bad_request"})
    return jsonify({"state": "okay"})

@app.route("/spam_filter/get_data", strict_slashes=False, methods=['GET'])
def retieve_data():
    """ get all data from the database """
    headers = request.headers
    print(headers)
    return jsonify({"states": "okay"})

@app.teardown_appcontext
def teardown(exc):
    """ hanle teardown_qppcontext """
    close_session()

@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)

