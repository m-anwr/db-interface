from model import Model


class Uses(Model):
    @classmethod
    def table_name(cls):
        return 'uses'

    @classmethod
    def table_primary_key(cls):
        return ["driver_national_id", "emergency_vehicle_id"]
