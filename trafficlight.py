from model import Model


class Trafficlight(Model):
    @classmethod
    def table_name(cls):
        return 'traffic_lights'

    @classmethod
    def table_primary_key(cls):
        return 'id'
