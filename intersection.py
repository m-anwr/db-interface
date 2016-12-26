from model import Model


class Intersection(Model):
    @classmethod
    def table_name(cls):
        return 'intersections'

    @classmethod
    def table_primary_key(cls):
        return 'mac'
