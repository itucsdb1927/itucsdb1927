from flask import Flask

import psycopg2 as db

from . import DB_URI
from util import fill_with_dummy_data


app = Flask(__name__)


@app.route("/")
def home_page():
    fill_with_dummy_data()

    with db.connect(DB_URI) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DUMMY")
        values = cur.fetchall()
        cur.close()

    values = [str(v[0]) for v in values]
    return "<br/>".join(values)


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
