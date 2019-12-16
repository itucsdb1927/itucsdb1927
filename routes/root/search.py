from flask import session, render_template, redirect, current_app

from models.user import User
from util import user_logged_in

from routes.root import root_blueprint


@root_blueprint.route("/search")
def search():
    user = None
    if user_logged_in():
        user = User.get_from_id(session['user_id'])

    # todo: implement search page

    return
