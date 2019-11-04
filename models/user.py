from dataclasses import dataclass

import psycopg2 as db

# from .. import DB_URI

DB_URI = "postgres://postgres:docker@localhost:5432/postgres"

@dataclass
class User:
    """
    Represents a single entry in the users table.

    Use the from_id method to get the row in the table.
    """
    id_: int
    creator: int
    avatar: str
    username: str
    email_address: str
    password: str
    first_name: str
    last_name: str
    is_admin: bool

    @classmethod
    @property
    def _table_name(cls):
        return "user"

    @classmethod
    def from_id(cls, id_):
        """Fetch the row with the specified id in the users table"""
        table_name = "users"
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table_name} WHERE id=%s", (id_,))
                fetched = cur.fetchone()
                print(fetched)
                return User(*fetched)

    def save(self, id_=None):
        """Save to table. id_=None will update the same row if it is a new object, will create a new one."""
        raise NotImplemented()