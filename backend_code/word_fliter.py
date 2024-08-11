#!/usr/bin/python3
"""
This module the content of the email will be filtered by words
and check if it is a spam or ham
"""
import json
from backend_code.database.data_operations import insert_data, get_data_with_email



symbols = [']', '[', '?', '!', ',', ':', '.', '@', '#', '$', '%', '^', '&', '(', ')', '-', '+', '*', '/', '~']
def delete(content):
    """ delete all the spaces and symbols from the content """
    new_content = ""
    for char in content:
        if char not in symbols:
            new_content += char
    return new_content.split(" ")


def words_filter(content="", email=""):
    """ 
    check if the email is spam or ham
    we are gonna open the file which has all percentages of the whole words
    and the percentages of the spam emails and ham emails
    after that we gonna calculate the spam_percentage of words in email
    and calculate the ham_percentage of words in email
    and after that compare both of them and we are gonna decide depending on 
    the bigger percentage
    """
    spam_words = []
    with open("prob.json", mode="r", encoding="utf-8") as file:
        info = json.loads(file)
        for spam_word in info:
            if spam_word != "spam_emails_percentage" and spam_word != "ham_emails_percentage":
                spam_words.append(spam_word)

    content = delete(content)
    percentage_ham = float(info["spam_emails_percentage"])
    percentage_spam = float(info["ham_emails_percentage"])
    result = ""
    
    for word in content:
        word = word.lower()
        if word in spam_words:
            percentage_ham *= float(info[word]["ham_percentage"])
            percentage_spam *= float(info[word]["spam_percentage"])

    if percentage_spam > percentage_ham:
        result = "Spam Email"
    else:
        result = "Not spam Email"

    return result, percentage_ham, percentage_spam
