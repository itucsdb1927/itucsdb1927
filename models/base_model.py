from dataclasses import dataclass
from copy import deepcopy

import inflection
import psycopg2 as db

# from .. import DB_URI

DB_URI = "postgres://postgres:docker@localhost:5432/postgres"

@dataclass
class BaseModel:
    id_: int        # IMPORTANT: None for new entry, otherwise use get_by_id.

    def __post_init__(self):
        """
        Copy initial values of model to compare with the current one
        and update only changed columns
        :return:
        """
        self._original_values = deepcopy(self.__dict__)

    @classmethod
    def get_from_id(cls, id_):
        _infered_table_name = inflection.underscore(inflection.pluralize(cls.__name__))
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {_infered_table_name} WHERE id=%s", (id_,))
                fetched = cur.fetchone()
                print(fetched)
                return cls(*fetched)

    def save(self):
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                if self.id_ is None:
                    self._create(cur)
                else:
                    self._update(cur)

    def _create(self, cur):
        _infered_table_name = inflection.underscore(inflection.pluralize(self.__class__.__name__))

        initial_values = deepcopy(self.__dict__)
        initial_values.pop('id_')
        initial_values.pop('_original_values')

        _columns_string = "(" + ", ".join([column for column in list(initial_values.keys())]) + ")"
        _values_string = f"({', '.join(['%s', ] * len(initial_values))})"
        cur.execute(
            f"INSERT INTO {_infered_table_name} "
            f"{_columns_string} "
            f"VALUES {_values_string} "
            "RETURNING id",
            tuple(list(initial_values.values()))
        )
        self.id_ = cur.fetchone()[0]

    def _update(self, cur):
        """
        Depends on original values.
        :param cur:
        :return:
        """
        _infered_table_name = inflection.underscore(inflection.pluralize(self.__class__.__name__))

        diff = {}
        for key in list(self._original_values.keys()):
            if self.__dict__[key] != self._original_values[key]:
                diff[key] = self.__dict__[key]

        set_string = ", ".join([f"{i if i != 'id_' else 'id'} = %s" for i in diff.keys()])
        values = tuple(list(diff.values()) + [self.id_, ])

        cur.execute(
            f"UPDATE {_infered_table_name} "
            f"SET {set_string} "
            f"WHERE id = %s",
            values
        )

    # todo: delete

    # todo: referenced joins
