from dataclasses import dataclass

import psycopg2 as db

from proj_config import DB_URI
from models.base_model import BaseModel
from models.exceptions import NoEntryError


@dataclass
class User(BaseModel):
    creator: int
    image_file: int
    username: str
    email_address: str
    password: str
    first_name: str
    last_name: str
    is_admin: bool

    @classmethod
    def get_from_username(cls, username):
        _infered_table_name = cls._infer_table_name()
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {_infered_table_name} WHERE username=%s", (username,))
                fetched = cur.fetchone()
                if fetched is None:
                    raise NoEntryError(f"No entry with the requested username = {username}")
                return cls(*fetched)
