#!/usr/bin/python3
""" 
module which has all functions of user
which can be applied to database
"""
from sqlalchemy.orm import sessionmaker, Session
from backend_code.database.database_table import engine, Email, User, User_Email
from sqlalchemy.exc import SQLAlchemyError
from backend_code.database.data_operations import session

classes_list = {'User': User, 'Email': Email, 'User_Email': User_Email}

def get_user_data_id(user_id):
    """ get the user data using the user_id """
    if type(user_id) is str:
        user_data = {}
        try:
            user = session.query(User).filter(User.id == user_id).all()
            if len(user) != 0:
                user_data["email_address"] = user[0].email_address
                user_data["name"] = user[0].name
                user_data["photo_url"] = user[0].photo_url
                return user_data
        except SQLAlchemyError as e:
            print(e)
    return None


def update_user_data_id(user_id, data):
    """ get the user data using the user_id """
    if type(user_id) is str and type(data) is dict:
        try:
            user = session.query(User).filter(User.id == user_id).all()
            allowed_data = ['name', 'photo_url']

            if len(user) != 0:
                for key, value in data.items():
                    if key in allowed_data:
                        setattr(user[0], key, value)
                session.commit()
                return user[0]
        except SQLAlchemyError as e:
            print(e)
    return None


def delete_user_data(user_id):
    """ delete the user using the user_id """
    if type(user_id) is str:
        try:
            result = session.query(User_Email).filter_by(user_id=user_id).delete()

            result_1 = session.query(User).filter_by(id=user_id).delete()
            if result_1 == 0:
                return None

            session.commit()
            return "okay"
        except SQLAlchemyError as e:
            print(e)
    return None


def get_user_data_email_username(email_address):
    """ get the user data using the email and user_name """
    if type(email_address) is str:
        user_data = {}
        try:
            user = session.query(User).filter(User.email_address == email_address).all()
            if len(user) != 0:
                user_data["email_address"] = user[0].email_address
                user_data["name"] = user[0].name
                user_data["user_id"] = user[0].id
                return user_data
        except SQLAlchemyError as e:
            print(e)
    return None

