#!/usr/bin/python3
""" 
module which has all functions of user
which can be applied to database
"""
from sqlalchemy.orm import sessionmaker, Session
from backend_code.database.database_table import engine, Email, User, User_Email
from sqlalchemy.exc import SQLAlchemyError


Session = sessionmaker(bind=engine)
session = Session()

classes_list = {'User': User, 'Email': Email, 'User_Email': User_Email}

def get_user_data(user_id):
    """ get the user data using the user_id """
    if type(user_id) is str:
        user_data = {}
        try:
            user = session.query(User).filter(User.id == user_id).all()
            if len(user) != 0:
                user_data["email_address"] = user[0].email_address
                user_data["name"] = user[0].name
                user_data["user_id"] = user[0].id
                return user_data
        except SQLAlchemyError as e:
            print(e)
    return None

def delete_user_data(user_id):
    """ delete the user using the user_id """
    if type(user_id) is str:
        try:
            result = session.query(User_Email).filter_by(user_id=user_id).delete()
            if result == 0:
                return None

            result_1 = session.query(User).filter_by(id=user_id).delete()
            if result_1 == 0:
                return None

            session.commit()
            return "okay"
        except SQLAlchemyError as e:
            print(e)
    return None
