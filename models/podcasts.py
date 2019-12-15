from dataclasses import dataclass

import psycopg2 as db
from datetime import datetime

from proj_config import DB_URI
from models.base_model import BaseModel
from models.user import User


@dataclass
class Podcasts(BaseModel):
    maintainer: int
    name: str
    genre: str
    description: str
    website_url: str
    date_created: datetime

    @classmethod
    def search(cls, string):
        _infered_table_name = cls._infer_table_name()
        pattern = f"%{string.strip()}%"
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {_infered_table_name} WHERE name ILIKE %s", (pattern,))
                for row in cur:
                    yield cls(*row)
                return

    def get_maintainer(self):
        return User.get_from_id(self.maintainer)
