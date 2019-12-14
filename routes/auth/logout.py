from flask import session

from . import auth_blueprint

from util import user_logged_in


from datetime import datetime

from flask import (
    session,
    render_template,
    redirect,
    url_for,
    current_app
)

from util import user_logged_in

from routes.auth import auth_blueprint


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    # todo: flash
    if user_logged_in():
        session.pop("user_id", None)
    return redirect("/")
