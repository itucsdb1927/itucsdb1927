from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextAreaField,
    IntegerField,
    SubmitField,
    validators,
)


class EpisodeForm(FlaskForm):
    title = StringField(
        'Title', validators=[validators.DataRequired(), validators.length(max=64)]
    )
    duration = IntegerField(
        'Duration (in minutes)',
        validators=[validators.DataRequired(), validators.NumberRange(min=1)],
    )
    summary = TextAreaField('Summary', validators=[validators.DataRequired()])
    episode_number = IntegerField(
        'Episode number',
        validators=[validators.DataRequired(), validators.NumberRange(min=0)],
    )
    submit = SubmitField('Create')
