#!/usr/bin/python3
""" blue print api """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/spam_filter')

from backend_code.user import *
from backend_code.user_email import *
