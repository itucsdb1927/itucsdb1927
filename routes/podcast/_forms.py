from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    validators,
)


class PodcastCreateForm(FlaskForm):
    name = StringField(
        'Name', validators=[validators.DataRequired(), validators.length(max=64)]
    )
    genre = StringField(
        'Genre', validators=[validators.DataRequired(), validators.length(max=32)],
    )
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    website_url = StringField('Website', validators=[validators.DataRequired()])
    submit = SubmitField('Create')


class PodcastEditForm(FlaskForm):
    genre = StringField(
        'Genre', validators=[validators.DataRequired(), validators.length(max=32)],
    )
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    website_url = StringField('Website', validators=[validators.DataRequired()])
    submit = SubmitField('Create')
