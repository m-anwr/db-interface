from abc import ABC, abstractclassmethod
from db_init import conn


class Model(ABC):
    def __init__(self, data={}):
        self.data = data

    @abstractclassmethod
    def table_name(cls):
        pass

    @classmethod
    def table_columns(cls):
        cursor = conn.execute("SELECT * FROM {};".format(cls.table_name()))
        return list(map(lambda x: x[0], cursor.description))

    @classmethod
    def find(cls, column, value):
        col_names = cls.table_columns()

        if column not in col_names:
            return None

        cursor = conn.execute(
            "SELECT * FROM {} WHERE {} = ? LIMIT 1".format(
                cls.table_name(),
                column
            ), [value])

        row = cursor.fetchone()

        if row is None:
            return None

        data = {}
        for info in zip(col_names, row):
            data[info[0]] = info[1]

        return cls(data)

    @classmethod
    def _construct_objects_from_cursor(cls, cursor):
        col_names = cls.table_columns()
        objects = []
        for row in cursor:
            data = {}
            for info in zip(col_names, row):
                data[info[0]] = info[1]
            objects.append(cls(data))

        return objects

    @classmethod
    def all(cls):
        cursor = conn.execute("SELECT * FROM {};".format(cls.table_name()))
        return cls._construct_objects_from_cursor(cursor)

    @classmethod
    def where(cls, filters={}):
        if not filters:
            return cls.all()

        keys = list(filters.keys())
        vals = list(filters.values())

        where_format = " AND ".join(
            list(map(lambda x: "{} = ?".format(x), keys))
        )

        cursor = conn.execute("SELECT * FROM {} WHERE {};".format(
            cls.table_name(),
            where_format
        ), vals)

        return cls._construct_objects_from_cursor(cursor)

    def save(self):
        if not self.data:
            return

        cols = list(self.data.keys())
        vals = tuple(self.data.values())

        conn.execute("INSERT INTO {} ({}) VALUES ({})".format(
            self.table_name(), ",".join(cols), ",".join(['?'] * len(cols))
        ), vals)

        conn.commit()
