#!/usr/bin/python3
""" user api """
from backend_code import app_views
from backend_code.database.data_operations import insert_data
from backend_code.database.user_operations import get_user_data_id, update_user_data_id, delete_user_data
from flask import jsonify, request
from jwt_encoding_decoding_method import verify_jwt 

@app_views.route('/new_user',  methods=['POST'], strict_slashes=False)
def add_user():
    """ add_new_user """
    data = request.json
    if "email_address" not in data or "name" not in data or "photo_url" not in data: 
        return jsonify({"state": "data missing"}), 400

    user = insert_data('User', data)

    if user == "user_already_exist":
        return jsonify({"state": "user_already_exist"})
    
    return jsonify({"user_id": user.id}), 200

@app_views.route('/new_user_info', methods=['PUT'], strict_slashes=False)
def update_user_info():
    """ update user info """
    request_data = request.json
    if "user_id" not in request_data and "name" not in request_data and "photo_url" not in request_data :
        return jsonify({"state": "data missing"}), 400

    user_id = request_data["user_id"]
    user = update_user_data_id(user_id, request_data)
    
    if user is None:
        return jsonify({"state": "user not found"}), 404

    return jsonify({"user_id": user.id}), 200


@app_views.route('/user_info', methods=['GET'], strict_slashes=False)
def get_user_info():
    """ get user info"""

    jwt_token = request.cookies.get('token')
    data = None

    if jwt_token is not None:
        data = verify_jwt(jwt_token)

    if jwt_token is None or data is None:
        return jsonify({'state': 'not authenticated'}), 401

    user_id = data["data_1"]
    user_info = get_user_data_id(user_id)

    if user_info is None:
        return jsonify({"state": "user not found"}), 404

    return jsonify({"user_info": user_info}), 200


@app_views.route('/user_not_exist', methods=['DELETE'], strict_slashes=False)
def delete_user_info():
    """ delete user """

    jwt_token = request.cookies.get('token')
    data = None
    print(jwt_token)
    if jwt_token is not None:
        data = verify_jwt(jwt_token)
    print(data)
    if jwt_token is None or data is None:
        return jsonify({'state': 'not authenticated'}), 401

    user_id = data["data_1"]
    result = delete_user_data(user_id)

    if result is None:
        return jsonify({"state": "user not found"}), 404

    return jsonify({"user_info": result}), 200

