from flask import session, render_template, redirect, current_app

from models.user import User
from util import user_logged_in

from routes.root import root_blueprint


@root_blueprint.route("/")
def home_page():
    user = None
    if user_logged_in():
        user = User.get_from_id(session['user_id'])
    return render_template("root/home.html", user=user, page_title="Home")
