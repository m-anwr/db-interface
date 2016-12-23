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
    def all(cls):
        col_names = cls.table_columns()
        cursor = conn.execute("SELECT * FROM {};".format(cls.table_name()))
        objects = []
        for row in cursor:
            data = {}
            for info in zip(col_names, row):
                data[info[0]] = info[1]
            objects.append(cls(data))
        return objects

    def save(self):
        if not self.data:
            return

        cols = list(self.data.keys())
        vals = tuple(self.data.values())

        conn.execute("INSERT INTO {} ({}) VALUES ({})".format(
            self.table_name(), ",".join(cols), ",".join(['?'] * len(cols))
        ), vals)

        conn.commit()
