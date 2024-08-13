#!/usr/bin/python3
""" module of email table """


import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, SmallInteger
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from uuid import uuid4


engine = create_engine("mysql://root:Ahmede2*@localhost/hbnb_dev_db", pool_size=10, max_overflow=20)
Base = declarative_base()


class Email(Base):
    """ initialize the email table """
    __tablename__ = 'emails'
    id = Column(String(60), primary_key=True, index=True)
    email_address = Column(String(225), nullable=False, unique=True)
    ip_address = Column(String(1000))
    created_on = Column(DateTime(), default=datetime.now)
    relationship('User_Email', cascade='all, delete-orphan', backref='email')

    def __init__(self, **kwargs):
        """ intilize email """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = uuid4()


class User(Base):
    """ initialize the user table """
    __tablename__ = 'users'
    id = Column(String(60), primary_key=True, index=True)
    name = Column(String(60), nullable=False)
    email_address = Column(String(225), nullable=False, unique=True)
    created_on = Column(DateTime(), default=datetime.now)
    relationship('User_Email', cascade='all, delete-orphan', backref='user')

    def __init__(self, **kwargs):
        """ intilize user """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = uuid4()


class User_Email(Base):
    """ user_product """
    __tablename__ = 'user_email'
    id = Column(String(60), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.id'), index=True)
    email_id = Column(String(60), ForeignKey('emails.id'), index=True)
    created_on = Column(DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        """ intilize user_email """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.id = uuid4()



Base.metadata.create_all(engine)
