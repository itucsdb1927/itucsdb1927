from flask import Flask

from routes.auth import auth_blueprint

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix="/auth")


@app.route("/")
def home_page():
    return "TODO: Implement"


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
    app.run()
