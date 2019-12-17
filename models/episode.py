from dataclasses import dataclass
from datetime import datetime, timedelta

import psycopg2 as db

from models.podcast import Podcast
from proj_config import DB_URI

from models.base_model import BaseModel
from models.exceptions import NoEntryError


@dataclass
class Episode(BaseModel):
    podcast: int
    title: int
    date: datetime
    duration: timedelta
    summary: str
    episode_number: int

    @property
    def minutes(self):
        return f"{self.duration.seconds//60}"

    @classmethod
    def get_all_for_podcast(cls, podcast_id):
        # todo: order by episode number
        _infered_table_name = cls._infer_table_name()
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"SELECT * FROM {_infered_table_name} WHERE podcast=%s",
                    (podcast_id,),
                )
                if cur.rowcount <= 0:
                    return []
                return [cls(*row) for row in cur]

    def get_podcast(self):
        return Podcast.get_from_id(self.podcast)
