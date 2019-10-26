from util import get_db_url, fill_with_dummy_data

from flask import Flask

import psycopg2 as db


app = Flask(__name__)


@app.route("/")
def home_page():
    fill_with_dummy_data(get_db_url())

    with db.connect(get_db_url()) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM DUMMY")
        values = cur.fetchall()
        cur.close()

    values = [str(v[0]) for v in values]
    return "<br/>".join(values)


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
