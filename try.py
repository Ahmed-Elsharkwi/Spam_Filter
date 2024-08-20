#!/usr/bin/python3

from backend_code.database.data_operations import insert_data, close_session, get_data_with_email, get_emails_data, session
from backend_code.database.user_email_operations import get_user_email_data, update_user_email_data, delete_user_email_data
from backend_code.database.user_operations import get_user_data_id, update_user_data_id
from sqlalchemy.exc import SQLAlchemyError
import asyncio

try:

        #data = {"user_id": "f0b4b88b-0de6-4b3a-858c-74c9eee07209", "email_id": "240de84a-66aa-49f4-a1c2-41ac26c53fc0"}
        data = {"email_address": "meoe@gmail.com"}
        email = insert_data("Email", data)

        content = get_user_email_data("d265e85c-ec6b-48a1-8ae2-f9b57b170532")
        print("befor:", content)
        print("email_id:", email.id)
        print(type(insert_data('User_Email', {"user_id": "d265e85c-ec6b-48a1-8ae2-f9b57b170532", "email_id": email.id}).id))

        content = get_user_email_data("d265e85c-ec6b-48a1-8ae2-f9b57b170532")
        data = get_emails_data()
        print("emails in emails tabel", data)
        print("after:", content)
        close_session()

except SQLAlchemyError as e:
    print("An error occurred while handling the database operation.")
    print(str(e))
