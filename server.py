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


if __name__ == "__main__":
    app.run()
