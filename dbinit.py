import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    'DROP TABLE IF EXISTS public.users CASCADE',
    'DROP TABLE IF EXISTS public.episodes CASCADE',
    'DROP TABLE IF EXISTS public.podcasts CASCADE',

    """
    create table users
    (
        id            serial       not null
            constraint users_pk
                primary key,
        username      varchar(64)  not null,
        email_address varchar(320) not null,
        password      varchar(60)  not null,
        first_name    varchar(64)  not null,
        last_name     varchar(64)  not null,
        is_admin      boolean      not null
    );
    """,

    """
    create unique index users_username_uindex
        on users (username);
    """,

    """
    create unique index users_email_address_uindex
        on users (email_address);
    """,

    """
    create table podcasts
    (
        id           serial      not null
            constraint podcasts_pk
                primary key,
        maintainer   integer
            constraint podcasts_users_id_fk
                references users
                on update cascade on delete set null,
        name         varchar(64) not null,
        genre        varchar(32) not null,
        description  text        not null,
        website_url  text        not null,
        date_created timestamp   not null
    );
    """,

    """
    create table episodes
    (
        id             serial      not null
            constraint episodes_pk
                primary key,
        podcast        integer     not null
            constraint episodes_podcasts_id_fk
                references podcasts
                on update cascade on delete cascade,
        title          varchar(64) not null,
        date           timestamp   not null,
        duration       interval    not null,
        summary        text        not null,
        episode_number integer     not null
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
