import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    'DROP TABLE IF EXISTS public.users CASCADE',
    'DROP TABLE IF EXISTS public.episodes CASCADE',
    'DROP TABLE IF EXISTS public.creators CASCADE',
    'DROP TABLE IF EXISTS public.podcasts CASCADE',
    'DROP TABLE IF EXISTS public.audio_files CASCADE',
    'DROP TABLE IF EXISTS public.image_files CASCADE',
    'DROP TABLE IF EXISTS public.episodes_creators CASCADE',

    """
    CREATE TABLE users (
        id serial NOT NULL,
        creator int NOT NULL,
        image_file int NULL,
        username varchar(64) NOT NULL,
        email_address varchar(320) NOT NULL,
        password varchar(53) NOT NULL,
        first_name varchar(64) NOT NULL,
        last_name varchar(64) NOT NULL,
        is_admin boolean NOT NULL     
    );
    """,

    """
    CREATE TABLE episodes (
        id serial NOT NULL, 
        image_file int NULL,
        audio_file int NOT NULL,
        podcast int NOT NULL,
        title varchar(64) NOT NULL,
        date timestamp NOT NULL, 
        duration interval NOT NULL, 
        summary text NOT NULL, 
        episode_number int NOT NULL
    );
    """,

    """
    CREATE TABLE creators (
        id serial NOT NULL, 
        about text NOT NULL, 
        website_url varchar(64) NULL, 
        spotify_url varchar(64) NULL,
        apple_pcasts_url varchar(64) NULL,
        google_pcasts_url varchar(64) NULL
    );
    """,

    """
    CREATE TABLE podcasts (
        id serial NOT NULL, 
        episode int NOT NULL,
        name varchar(64) NOT NULL, 
        genre varchar(32) NOT NULL, 
        description text NOT NULL, 
        date_created timestamp NOT NULL
    );
    """,

    """
    CREATE TABLE audio_files (
        id serial NOT NULL, 
        is_local boolean NOT NULL, 
        path varchar(128) NOT NULL
    );
    """,

    """
    CREATE TABLE image_files (
        id serial NOT NULL, 
        is_local boolean NOT NULL, 
        path varchar(128) NOT NULL
    );
    """,

    """
    CREATE TABLE episodes_creators (
        id serial NOT NULL, 
        episode int NOT NULL, 
        creator int NOT NULL 
    );
    """,
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
