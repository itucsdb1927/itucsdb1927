from dataclasses import dataclass

import psycopg2 as db
from datetime import datetime

from models.episode import Episode
from proj_config import DB_URI
from models.base_model import BaseModel
from models.user import User


@dataclass
class Podcast(BaseModel):
    maintainer: int
    name: str
    genre: str
    description: str
    website_url: str
    date_created: datetime

    @property
    def episodes(self):
        return Episode.get_all_for_podcast(self.id_)

    @classmethod
    def search(cls, string):
        """
        Simple, case-insensitive search for podcasts.
        :param string: search string
        :return: list of Podcasts
        """
        _infered_table_name = cls._infer_table_name()
        pattern = f"%{string.strip()}%"
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM {_infered_table_name} WHERE name ILIKE %s",
                    (pattern,),
                )
                if cur.rowcount <= 0:
                    return []
                return [cls(*row) for row in cur]

    def get_maintainer(self):
        return User.get_from_id(self.maintainer)
