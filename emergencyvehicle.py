from model import Model


class EmergencyVehicle(Model):
    @classmethod
    def table_name(cls):
        return 'emergency_vehicles'

    @classmethod
    def table_primary_key(cls):
        return 'id'