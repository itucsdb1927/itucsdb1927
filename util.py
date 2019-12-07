from flask import session


def user_logged_in():
    return 'user_id' in session
