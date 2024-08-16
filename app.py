#!/usr/bin/python3
"""
the main module of the app
"""
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import requests
from backend_code.database.data_operations import close_session, get_data_with_email, get_emails_data, insert_data
from backend_code.database.user_operations import get_user_data_email_username, update_user_data_id
from backend_code.word_fliter import words_filter
from flask import Flask, make_response, jsonify, request, render_template, make_response
from flask_cors import CORS
import re
from validate import validate
from jwt_encoding_decoding_method import create_jwt
from datetime import datetime, timedelta



app = Flask(__name__)

app.secret_key = 'i am good'
google_client_id = '616226883527-al4o834funvq9v121lpnuaorqnrpn2u1.apps.googleusercontent.com'
google_client_secret = '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'
google_redirect_uri = 'http://localhost:5000/authorize'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=google_redirect_uri,
    client_kwargs={'scope': 'email profile'},
)


@app.route('/login')
def login():
    if request.cookies.get('token') is None:
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri, prompt='consent')
    else:
        return redirect(url_for('landing_page'))

@app.route('/authorize')
def authorize():
    try:
        token = google.authorize_access_token()
        session['google_token'] = token
        google_token = session['google_token']
        resp = (google.get('https://www.googleapis.com/oauth2/v1/userinfo', token=google_token)).json()
        print(resp["email"])
        data = get_user_data_email_username(resp["email"])
        print(data)
        if data is None:
            google_data = {
                    "email_address": resp["email"], 
                    "name": resp["name"], 
                    "photo_url": resp["picture"]
                    }

            new_user = insert_data("User", google_data)
            user_id = new_user.id
        else:
            user_object = update_user_data_id(data["user_id"], resp["name"], resp["picture"])
            user_id = user_object.id

        token = create_jwt({"data_1": user_id, 'exp': datetime.utcnow() + timedelta(seconds=30)})
        response = make_response(jsonify({"status": "okay"}), 200)
        response.set_cookie('token', token, httponly=True)
        return response
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return jsonify({"status": "okay"}), 200

@app.route("/", strict_slashes=False, methods=['GET'])
def landing_page():
    """ return the landing page"""
    img_source = "/static/spam.jpg"
    return render_template("landing_page.html", img_source=img_source)


@app.route("/spam_filter", strict_slashes=False, methods=['GET'])
def reder_filter_page():
    """ reder the main page of spam filter """
    return render_template("spam_filter.html")

@app.route("/spam_filter/check", strict_slashes=False, methods=['POST'])
def filter_content():
    """ filter the content and decide if the email is spam or ham """
    valid = validate(request.json["email"], request.json["content"])
    if (valid != "okay"):
        return jsonify({"state": valid})
    dict = {}
    result = ""
    output = None
    for item in request.json:
        dict[item] = request.json[item]
    
    result, ham, spam = words_filter(dict["content"], dict["email"])

    if result != "Spam Email":
        output = get_data_with_email(dict["email"])
        if output is not None:
            result = "Spam Email"

    return jsonify({"state": result, "spam": spam, "ham": ham})

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
    return jsonify(get_data())

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

