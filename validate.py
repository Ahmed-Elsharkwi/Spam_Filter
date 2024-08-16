#!/usr/bin/python3
import re
"""
it is the validation module which will validate the format of email and content
"""


def validate(email, content):
    """ 
    validate the email format which is suitable to a spesific regex and also check 
    the length of email which should be at least 10 words
    """
    if email and content:
       
        pattern = r"[\w-]{5,}(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}"
        result = re.match(pattern, email)
        if result is None:
            return "please Enter a valid email"
        content = re.sub(r"[^a-zA-Z\s]", '', content)
        content = content.split(" ")
        if result and len(content) < 10:
            return "please Enter at least ten words in the content box"
    else:
        return "All fields must be filled out"
    
    return "okay"
