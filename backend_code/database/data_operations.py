#!/usr/bin/python3
""" 
module which has all functions of operations 
which can be applied to database 
"""
from sqlalchemy.orm import sessionmaker, Session
from backend_code.database.database_table import engine, Email, User, User_Email
from sqlalchemy.exc import SQLAlchemyError


Session = sessionmaker(bind=engine)
session = Session()

classes_list = {'User': User, 'Email': Email, 'User_Email': User_Email}
def insert_data(class_name, data):
    """ insert data into data base """
    new_object = None

    if class_name in classes_list and type(data) is dict:
        try:
            new_object = classes_list[class_name](**data)
            session.add(new_object)
            session.commit()
        except SQLAlchemyError as e:
            print(e)
    return new_object

def get_data_with_email(user_id = "", email=""):
    """ 
    it will check if that email exists in the emails table
    and it will check if that email is related to user_id which was
    given and after that it will return the email id
    we did all that to check if the email is blocked by that user or not
    using the email addres
    """
    email_data = None

    if type(user_id) is str and type(email) is str:
        try:
            data = session.query(Email).filter(Email.email_address == email).first()
            if data is not None:
                content = session.query(User_Email).filter(
                        User_Email.user_id == user_id, 
                        User_Email.email_id == data.id).all()
                if len(content) != 0:
                    email_data = data
        except SQLAlchemyError as e:
            print(e)
    return email_data


def get_emails_data():
    """ get the whole data of all emails from the email table"""
    data_dict = {"email_address": [], "ip": [], "created_date": []}
    try:
        data = session.query(Email).all()
        for item in data:
            data_dict["email_address"].append(item.email_address)
            data_dict["ip"].append(item.ip_address)
            data_dict["created_date"].append(item.created_on)
    except SQLAlchemyError as e:
        data_dict = None
    return data_dict

def close_session():
    """ remove the session """
    session.close()
