from decimal import Decimal
from typing import Any
from django.db import models, connection
from django.conf import settings
from django.db.models import Func, Value
from .get_schema import get_current_schema
from .database_encryption import AesEncrypt, AesDecrypt, DatabaseUtils
#from django.db.models import F

# # Encrypting a field
# MyModel.objects.update(encrypted_field=AesEncrypt(F('plain_text_field'), 'my_secret_key'))

# # Decrypting a field in a query
# decrypted_values = MyModel.objects.annotate(decrypted_field=AesDecrypt(F('encrypted_field'), 'my_secret_key')).values('decrypted_field')

class EncryptedTextField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.db_utils = DatabaseUtils()
        self.all_keys = self.db_utils.get_keys()
        self.encrypt_key = self.all_keys[0]
        self.schema = get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value    

class EncryptedCharField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        self.schema = get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value  

class EncryptedEmailField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        self.schema = get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value 

class EncryptedIntegerField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        self.schema = get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value  

class EncryptedFloatField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        self.schema = get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value 

class EncryptedDecimalField(models.BinaryField):
    def __init__(self, *args, **kwargs):
        self.encrypt_key = settings.PGCRYPTO_KEY
        self.schema = get_current_schema()
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_encrypt(%s::text, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return cursor.fetchone()[0]
        return value 

    def from_db_value(self, value, expression, connection):
        if value is not None:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {self.schema}.pgp_sym_decrypt(%s::bytea, %s::text)", [value, self.encrypt_key])
                return Decimal(cursor.fetchone()[0])
        return value  

