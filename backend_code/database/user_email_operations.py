#!/usr/bin/python3
""" 
module which has all functions of user_email_table
which can be applied to database 
"""
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker, Session
from backend_code.database.database_table import engine, Email, User, User_Email
from sqlalchemy.exc import SQLAlchemyError


Session = sessionmaker(bind=engine)
session = Session()

classes_list = {'User': User, 'Email': Email, 'User_Email': User_Email}

def get_user_email_data(user_id):
    """ get the emails which are related to the user """
    data_dict = None

    if type(user_id) is str:
        try:
            emails_ids = []
            data = session.query(User_Email).filter_by(user_id=user_id).all()

            if len(data) != 0:

                for item in data:
                    emails_ids.append(item.email_id)

                emails = session.query(Email).filter(Email.id.in_(emails_ids)).all()

                if len(emails) != 0:
                    data_dict = {}
                    for email in emails:
                        data_dict[f"{email.id}"] = {
                                "email_address": email.email_address, 
                                "created_date": email.created_on
                                }
        except SQLAlchemyError as e:
            data_dict = None
    return data_dict


def update_user_email_data(user_id, old_email_id, new_email_id):
    """ update the blocked email  with user_id and email_id """
    try:
        if type(user_id) is str and type(
                old_email_id) is str and type(new_email_id) is str:
            result = session.query(User_Email).filter_by(user_id=user_id, email_id=old_email_id).first()
            if result is not None:
                result.email_id = new_email_id
                session.commit()
                return new_email_id

    except SQLAlchemyError as e:
        print(e)
    return None

def delete_user_email_data(user_id, email_id):
    """ delete the user and the email using the user_id and the email id"""
    if type(user_id) is str and type(old_email_id) is str:
        try:
            result = session.query(User_Email).filter_by(
                user_id=user_id, email_id=email_id).delete()
            if result == 0:
                return None


            session.commit()
            return "okay"
        except SQLAlchemyError as e:
            print(e)
    return None
