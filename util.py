import os
import psycopg2 as db


def fill_with_dummy_data(db_url):
    """
    To test the database connection and fill with values.
    Will be removed later on.
    :param db_url:
    :return:
    """
    numbers = [12, 50, 420, 3, 30, 999]
    with db.connect(db_url) as conn:
        cursor = conn.cursor()
        for number in numbers:
            cursor.execute("INSERT INTO DUMMY VALUES (%s)", (number,))
        cursor.close()
