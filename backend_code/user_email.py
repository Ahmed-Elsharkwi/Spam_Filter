#!/usr/bin/python3
""" user api """
from backend_code import app_views
from backend_code.database.user_email_operations import get_user_email_data, update_user_email_data, delete_user_email_data
from backend_code.database.data_operations import insert_data, get_emails_data
from flask import jsonify, request
from jwt_encoding_decoding_method import verify_jwt
import re


@app_views.route('/new_email',  methods=['POST', 'PUT'], strict_slashes=False)
def add_email():
    """ add new blocked email and update old blocked email"""
    jwt_token = request.cookies.get('token')
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({'state': 'not authenticated'}), 401

    user_id = data['data_1']
    email_address = request.json["email_address"]
    pattern = r"[\w-]{5,}(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}"
    result = re.match(pattern, email_address)

    if email_address is not None and result:

        emails_list = get_emails_data()

        if emails_list is None or email_address not in emails_list:
            email_id = insert_data('Email', {'email_address': email_address}).id
        else:
            email_id = emails_list[email_address]['email_id']
        
        email_dict = get_user_email_data(user_id)

        if email_dict is None or email_id not in email_dict:

            if request.method == "PUT":

                if "old_id" in request.json:
                    old_id = request.json['old_id']
                    update_user_email_data(user_id, old_id, email_id)
                else:
                    return jsonify({"state": "missing old_email_id"}), 400
            else:
                new_email = insert_data('User_Email', {'user_id': user_id, 'email_id': email_id})
        else:
            return jsonify({"state": "email already exists"}), 200

        return jsonify({"state": "email added"}), 200
    else:
        return jsonify({"state": "bad_request"}) , 400


@app_views.route('/user_emails', methods=['GET'], strict_slashes=False)
def get_user_emails():
    """ get all the emails which are blocked by the user """

    jwt_token = request.cookies.get('token')
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({'state': 'not authenticated'}), 401

    user_id = data['data_1']
    print(user_id)

    emails = get_user_email_data(user_id)

    if emails is not None:
        return jsonify(emails), 200
    else:
        return jsonify({"state": "there are not any blocked emails"}), 200


@app_views.route('/user_email_not_exist', methods=['DELETE'], strict_slashes=False)
def delete_email():
    """ delete an email which was blocked by the user """
    jwt_token = request.cookies.get('token')
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({'state': 'not authenticated'}), 401

    user_id = data['data_1']

    if "email_id" in request.json:
        email_id = request.json['email_id']
        respond = delete_user_email_data(user_id, email_id)
        return jsonify({"state": respond}), 200

    else:
        return jsonify({"state": "email_id is missing"}), 400
