from model import Model


class Street(Model):
    @classmethod
    def table_name(cls):
        return 'streets'
