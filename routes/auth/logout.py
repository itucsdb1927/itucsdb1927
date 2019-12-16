from flask import session, redirect

from routes.auth import auth_blueprint
from util import user_logged_in


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    # todo: flash
    if user_logged_in():
        session.pop("user_id", None)
    return redirect("/")
