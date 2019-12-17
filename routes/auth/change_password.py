from datetime import datetime

from flask import session, render_template, redirect, url_for, current_app, abort

from models.user import User
from util import user_logged_in

from routes.auth import auth_blueprint

from routes.auth._forms import ChangePasswordForm


@auth_blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if not user_logged_in():
        abort(401)

    form = ChangePasswordForm()

    if form.validate_on_submit():
        try:
            user = User.get_from_id(session['user_id'])
            bcrypt = current_app.config['BCRYPT']
            if bcrypt.check_password_hash(user.password, form.data['old']):
                user.password = (
                    bcrypt
                    .generate_password_hash(form.data['new'])
                    .decode('utf-8')
                )
                user.save()
                return redirect("/")
            else:
                abort(403)
        except:
            abort(500)

    return render_template("auth/change_password.html", form=form)
