from model import Model


class Trafficlight(Model):
    @classmethod
    def table_name(cls):
        return 'traffic_lights'
