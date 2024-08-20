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
import base64
from validate import validate
from jwt_encoding_decoding_method import create_jwt, verify_jwt
from datetime import datetime, timedelta



app = Flask(__name__)
CORS(app, supports_credentials=True)


app.secret_key = 'i am good'
google_client_id = '616226883527-al4o834funvq9v121lpnuaorqnrpn2u1.apps.googleusercontent.com'
google_client_secret = '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'
google_redirect_uri = 'http://localhost:8000/authorize'

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
        if request.args.get('next_page') is not None:
            session['next_page'] = request.args.get('next_page')
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
        data = get_user_data_email_username(resp["email"])

        if data is None:
            google_data = {
                    "email_address": resp["email"], 
                    "name": resp["name"], 
                    "photo_url": resp["picture"]
                    }

            new_user = insert_data("User", google_data)
            user_id = new_user.id
        else:
            user_object = update_user_data_id(data["user_id"],
                    {"name": resp["name"],
                        "photo_url": resp["picture"]})
            user_id = user_object.id

        token = create_jwt({"data_1": user_id, 'exp': datetime.utcnow() + timedelta(seconds=1200)})

        if 'next_page' in session:
            next_page = session['next_page']
            del session['next_page']
            response = make_response(redirect(next_page))
        
        elif 'next' in session:
            next_url = session['next']
            del session['next']
            response = make_response(redirect(next_url))
        else:
            response = make_response(jsonify({"status": "okay"}), 200)

        response.set_cookie('token', token, samesite='None', secure=True)
        return response

    except Exception as e:
        print(e)
        #return redirect('/')


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
    """
    jwt_token = request.cookies.get('token')
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        session['next'] = '/spam_filter'
        return redirect(url_for('login'))
    """
    return render_template("spam_filter.html")

@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)

