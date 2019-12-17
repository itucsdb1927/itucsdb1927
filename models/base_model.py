from dataclasses import dataclass
from copy import deepcopy
from typing import Optional

import inflection
import psycopg2 as db

from proj_config import DB_URI
from .exceptions import NoEntryError


@dataclass
class BaseModel:
    """BaseModel for database entries

    Usage:

    - Derive from this class with another dataclass
    - Add table columns names with matching names, orders and types
    - For new entries, instantiate class with constructor, marking id_=None
    - For fetching existing entries, call :meth:`get_from_id`
    - Make changes or keep as is, then call :meth:`save`.
    - Changes will be reflected in the database.

    """
    id_: Optional[int]  # IMPORTANT: None for new entry, otherwise use get_by_id.

    def __post_init__(self):
        """
        Copy initial values of model to compare with the current one
        and update only changed columns
        :return:
        """
        self._original_values = deepcopy(self.__dict__)

    @classmethod
    def _infer_table_name(cls):
        """Detect table name from the derived classes' name."""
        return inflection.underscore(inflection.pluralize(cls.__name__))

    @classmethod
    def get_from_id(cls, id_):
        _infered_table_name = cls._infer_table_name()
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {_infered_table_name} WHERE id=%s", (id_,))
                fetched = cur.fetchone()
                if fetched is None:
                    raise NoEntryError(f"No entry with the requested id = {id_}")
                # Classes are still objects in python
                # If this class is derived, `cls` references the derived class
                # and not the base class. So we can use the class object to instantiate.
                return cls(*fetched)

    def save(self):
        """Automatically commit changes

        If the model has been instantiated without an id,
        it is a new entry and an entry is created in the table.
        If :meth:`get_from_id` was used, only changed values are saved.
        """
        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                if self.id_ is None:
                    self._create(cur)
                else:
                    self._update(cur)

    def _create(self, cur):
        """
        Create a new entry in table.
        :param cur: Database cursor
        :return:
        """
        _infered_table_name = self._infer_table_name()

        # copy all variables
        initial_values = deepcopy(self.__dict__)
        # pop id_ and _original_values, to prevent interfering with SQL statement
        initial_values.pop('id_')
        initial_values.pop('_original_values')

        # Create the columns string, which does not include id
        _columns_string = (
            "(" + ", ".join([column for column in list(initial_values.keys())]) + ")"
        )
        # Create the values string, consisting of %s placeholders with the correct
        # amount for psycopg2 to fill in later.
        _values_string = f"({', '.join(['%s', ] * len(initial_values))})"
        cur.execute(
            f"INSERT INTO {_infered_table_name} "
            f"{_columns_string} "
            f"VALUES {_values_string} "
            "RETURNING id",
            tuple(list(initial_values.values())),
        )
        # update the id with SQL Query 'RETURNING id'
        self.id_ = cur.fetchone()[0]

    def _update(self, cur):
        """
        Update an existing entry in the table.
        Depends on original values and updates only differing fields of the model.
        :param cur: Database cursor
        :return:
        """
        _infered_table_name = self._infer_table_name()

        # for every original value, compare with the current self.__dict__.
        # if it is different, add to the differences dictionary
        diff = {}
        for key in list(self._original_values.keys()):
            if self.__dict__[key] != self._original_values[key]:
                diff[key] = self.__dict__[key]

        # if the diff is empty, no changes have been made
        # continuing further will generate invalid SQL statements.
        if not diff:
            return

        # match all column names and append them with =%s placeholder
        # produces a string like this: name = %s, description = %s, etc...
        set_string = ", ".join(
            [f"{i if i != 'id_' else 'id'} = %s" for i in diff.keys()]
        )
        # list values of the changed fields, with the same ordering as set_string
        # + entry id for changing the correct entry
        values = tuple(list(diff.values()) + [self.id_,])

        cur.execute(
            f"UPDATE {_infered_table_name} " f"SET {set_string} " f"WHERE id = %s",
            values,
        )

    def delete(self):
        if self.id_ is None:
            return

        _infered_table_name = self._infer_table_name()

        with db.connect(DB_URI) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"DELETE FROM {_infered_table_name} WHERE id = %s", (self.id_,)
                )
                # delete the entry, set the id_ to None, so calling save on
                # the model again recreates the entry with another id.
                self.id_ = None
