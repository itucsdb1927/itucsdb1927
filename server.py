import os

from flask import Flask, session, render_template
from flask_bcrypt import Bcrypt

from routes.auth import auth_blueprint
from models.user import User
from util import user_logged_in

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.urandom(32),
    WTF_CSRF_SECRET_KEY=os.urandom(32),
    BCRYPT=Bcrypt(app)
)
app.register_blueprint(auth_blueprint, url_prefix="/auth")


@app.route("/")
def home_page():
    user = None
    if user_logged_in():
        user = User.get_from_id(session['user_id'])


    return render_template("root.html", user=user, page_title="Home")


@app.route("/audio_test")
def audio_page():
    """
    Page for testing whether playing audio files served from static folder works correctly
    :return:
    """
    return """
    <audio controls>
        <source src="static/test_audio.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
    """


@app.route("/logo_test")
def logo_page():
    """
    Page for testing whether serving static files through flask works correctly.
    :return:
    """
    return """
    <img src="static/logo.png" alt="Audiocasts Logo" height="200">
    """


if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.urandom(32)
    app.run()
