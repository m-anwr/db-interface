from abc import ABC, abstractclassmethod
from db_init import conn


class Model(ABC):
    def __init__(self, data={}):
        self.data = data

    @abstractclassmethod
    def table_name(cls):
        pass

    @abstractclassmethod
    def table_primary_key(cls):
        pass

    @classmethod
    def table_columns(cls):
        cursor = conn.execute("SELECT * FROM {};".format(cls.table_name()))
        return list(map(lambda x: x[0], cursor.description))

    @classmethod
    def join(cls, other_instance, through_table, cls_fk, instance_fk):
        cursor = conn.execute(
            "SELECT * FROM {} JOIN {} ON {} = {} WHERE {} = ?".format(
                cls.table_name(),
                through_table,
                cls.table_name() + "." + cls.table_primary_key(),
                through_table + "." + cls_fk,
                through_table + "." + instance_fk
            ), [other_instance.data[other_instance.table_primary_key()]])

        return cls._construct_objects_from_cursor(cursor)

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

    @classmethod
    def where_range(cls, filters={}):
        if not filters:
            return cls.all()

        keys = list(filters.keys())
        vals = list(filters.values())

        where_format = ""
        for key in keys:
            if key[0] == "t":
                key = key[2:]
                where_format += "AND " + key + "<=? "
            elif key[0] == "f":
                key = key[2:]
                where_format += "AND " + key + ">=? "
            else:
                where_format += "AND " + key + "=? "

        where_format = where_format[3:]

        cursor = conn.execute("SELECT * FROM {} WHERE {};".format(
            cls.table_name(),
            where_format
        ), vals)

        return cls._construct_objects_from_cursor(cursor)

    def delete(self):
        conn.execute(
            "DELETE FROM {} WHERE {} = ?".format(
                self.table_name(),
                self.table_primary_key()
            ), [self.data[self.table_primary_key()]])

        conn.commit()

        return True

    def save(self):
        if not self.data:
            return False

        cols = list(self.data.keys())
        vals = tuple(self.data.values())

        conn.execute("INSERT INTO {} ({}) VALUES ({})".format(
            self.table_name(), ",".join(cols), ",".join(['?'] * len(cols))
        ), vals)

        conn.commit()

        return True

    def update(self, update_data={}):
        if not update_data:
            return False

        cols = list(update_data.keys())
        vals = list(update_data.values())

        set_format = ", ".join(
            list(map(lambda x: "{} = ?".format(x), cols))
        )

        conn.execute("UPDATE {} SET {} WHERE {} = {}".format(
            self.table_name(),
            set_format,
            self.table_primary_key(),
            self.data[self.table_primary_key()]
        ), vals)

        conn.commit()

        self.data.update(update_data)

        return True
