from datetime import datetime

from flask import session, render_template, redirect, current_app

from flask_bcrypt import Bcrypt

from models.user import User
from util import user_logged_in

from routes.auth import auth_blueprint
from routes.auth._forms import SignUpForm


@auth_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    if user_logged_in():
        redirect("/")

    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            id_=None,
            username=form.data['username'],
            email_address=form.data['email'],
            password=(
                current_app.config['BCRYPT']
                .generate_password_hash(form.data['password'])
                .decode('utf-8')
            ),
            first_name=form.data['first_name'],
            last_name=form.data['last_name'],
            is_admin=False,
        )
        try:
            user.save()
            session['user_id'] = user.id_
            print("You have signed up and logged in successfully")
            return redirect("/")
        except:
            print("Error")

    return render_template("auth/signup.html", form=form, page_title="Sign Up ")
