from datetime import datetime

from flask import (
    session,
    render_template,
    redirect,
    url_for
)

from util import user_logged_in

from routes.auth import auth_blueprint

from routes.auth._forms import LoginForm


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return "IMPLEMENT: Login Page"
