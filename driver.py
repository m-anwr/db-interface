from model import Model
import hashlib


class Driver(Model):
    def __init__(self, data={}):
        form_data = data
        pwd = form_data.pop('password', None)
        if pwd is not None:
            hash_object = hashlib.md5(pwd.encode('utf-8'))
            form_data['encrypted_password'] = hash_object.hexdigest()

        super().__init__(form_data)


    @classmethod
    def table_name(cls):
        return 'drivers'

    @classmethod
    def table_primary_key(cls):
        return 'national_id'
