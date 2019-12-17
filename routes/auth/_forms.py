from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    FileField,
    SubmitField,
    validators,
)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(),])
    password = PasswordField('Password', validators=[validators.DataRequired(),])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[validators.DataRequired(),])
    last_name = StringField('Last Name', validators=[validators.DataRequired(),])
    username = StringField('Username', validators=[validators.DataRequired(),])
    email = StringField(
        'Email Address', validators=[validators.DataRequired(), validators.Email()]
    )
    password = PasswordField('Password', validators=[validators.DataRequired(),])
    submit = SubmitField('Sign Up')


class ChangePasswordForm(FlaskForm):
    old = PasswordField('Old Password', validators=[validators.DataRequired()])
    new = PasswordField('New Password', validators=[validators.DataRequired()])
    submit = SubmitField('Change')
