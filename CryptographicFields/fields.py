from django.db import models
from django.core import checks, exceptions, validators
from.cryptography import Encrypter,Decrypter
import ast
from django.db.backends.utils import format_number
import decimal
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import NOT_PROVIDED
from timestring import Date
class BooleanField(models.BooleanField):
    def to_python(self,value):
        if isinstance(value,bytes):
            return value
        print('called my one')
        if value in (True, False):
            # 1/0 are equal to True/False. bool() converts former to latter.
            return Encrypter(bool(value))
        elif value in ('t', 'True', '1','T','Y','Yes','yes','y'):
            return Encrypter(True)
        elif value in ('f', 'False', '0','F','N','No','no','n'):
            return Encrypter(False)
        else:
            raise exceptions.ValidationError(
            self.error_messages['invalid_nullable' if self.null else 'invalid'],
            code='invalid',
            params={'value': value},
        )
    def get_prep_value(self, value):
        if value is None:
            return None
        return self.to_python(value)
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return ast.literal_eval(Decrypter(value).decode())
        else:
            return None
    
    def get_internal_type(self):
        return "BinaryField"
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

class CharField(models.CharField):
    def get_internal_type(self):
        return "BinaryField"

    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if isinstance(value, str) or value is None:
            return Encrypter(value)
        return Encrypter(str(value))

    def get_prep_value(self, value):
        return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

class DecimalField(models.DecimalField):
    def get_internal_type(self):
        return "BinaryField"
    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if value is None:
            return value
        if isinstance(value, float):
            return self.context.create_decimal_from_float(value)
        try:
            return decimal.Decimal(value)
        except (decimal.InvalidOperation, TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
    def get_db_prep_save(self, value, connection):
        return Encrypter(connection.ops.adapt_decimalfield_value(self.to_python(value), self.max_digits, self.decimal_places))
    def get_prep_value(self, value):
        return self.to_python(value)
    
    def get_db_prep_value(self, value, connection):
        return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return format_number(decimal.Decimal(Decrypter(value).decode()),self.max_digits,self.decimal_places)
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

class EmailField(models.EmailField):
    def get_internal_type(self):
        return "BinaryField"

    def to_python(self, value):
        print('caleed email')
        if isinstance(value, str) or value is None:
            validators.EmailValidator(value)
            return Encrypter(value)
        if isinstance(value,bytes):
            return value
    def get_prep_value(self, value):
        try:
            validators.validate_email(value)
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError('Invaild Email Address',
                code='invalid',
                params={'value': value},
            )
        else:
            return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    
class FilePathField(models.FilePathField):
    def get_internal_type(self):
        return "BinaryField"

    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return Encrypter(value)
        if isinstance(value,bytes):
            return value
        return Encrypter(str(value))

    def get_prep_value(self, value):
        return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

class FloatField(models.FloatField):
    def get_internal_type(self):
        return "BinaryField"

    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if value is None:
            return value
        try:
            return Encrypter(float(value))
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
   
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return float(Decrypter(value).decode())
        else:
            return None
    
    def get_prep_value(self, value):
        return self.to_python(value)
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    
class IntegerField (models.IntegerField):
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return int(Decrypter(value).decode())
        else:
            return None
    def get_prep_value(self, value):
        return self.to_python(value)
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value,bytes):
            return value
        try:
            return Encrypter(int(value))
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )
class BigIntegerField(IntegerField):
    description = _("Big (8 byte) integer")
    MAX_BIGINT = 9223372036854775807

    def get_internal_type(self):
        return "BigIntegerField"

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': -BigIntegerField.MAX_BIGINT - 1,
            'max_value': BigIntegerField.MAX_BIGINT,
            **kwargs,
        })
    

class GenericIPAddressField(models.GenericIPAddressField):
    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        value = value.strip()
        if ':' in value:
            validators.validate_ipv46_address(value)
            return clean_ipv6_address(value, self.unpack_ipv4, self.error_messages['invalid'])
        validators.validate_ipv46_address(value)
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return Encrypter(connection.ops.adapt_ipaddressfield_value(value))
    def get_prep_value(self, value):
        return self.to_python(value)
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
class PositiveBigIntegerField(models.PositiveBigIntegerField):
    negativeint=_('“%(value)s” value must be an positive integer.')
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return int(Decrypter(value).decode())
        else:
            return None
    def get_prep_value(self, value):
        return self.to_python(value)
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value,bytes):
            return value
        try:
            if int(value)>=0:
                return Encrypter(int(value))
            else:
                raise exceptions.ValidationError(
                self.negativeint,
                code='invalid',
                params={'value': value},
            )

        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )


class PositiveIntegerField(models.PositiveIntegerField):
    negativeint=_('“%(value)s” value must be an positive integer.')
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return int(Decrypter(value).decode())
        else:
            return None
    def get_prep_value(self, value):
        return self.to_python(value)
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value,bytes):
            return value
        try:
            if int(value)>=0:
                return Encrypter(int(value))
            else:
                raise exceptions.ValidationError(
                self.negativeint,
                code='invalid',
                params={'value': value},
            )

        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

class PositiveSmallIntegerField(models.PositiveSmallIntegerField):
    negativeint=_('“%(value)s” value must be an positive integer.')
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return int(Decrypter(value).decode())
        else:
            return None
    def get_prep_value(self, value):
        return self.to_python(value)
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value,bytes):
            return value
        try:
            if int(value)>=0:
                return Encrypter(int(value))
            else:
                raise exceptions.ValidationError(
                self.negativeint,
                code='invalid',
                params={'value': value},
            )

        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

class SlugField(models.SlugField):
    def get_internal_type(self):
        return "BinaryField"

    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if isinstance(value, str) or value is None:
            return Encrypter(value)
        return Encrypter(str(value))

    def get_prep_value(self, value):
        return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

class SmallIntegerField(models.SmallIntegerField):
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return int(Decrypter(value).decode())
        else:
            return None
    def get_prep_value(self, value):
        return self.to_python(value)
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value,bytes):
            return value
        try:
            return Encrypter(int(value))
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

class TextField(models.CharField):
    def get_internal_type(self):
        return "BinaryField"

    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if isinstance(value, str) or value is None:
            return Encrypter(value)
        return Encrypter(str(value))

    def get_prep_value(self, value):
        return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

class URLField(models.CharField):
    url=validators.URLValidator()
    def get_internal_type(self):
        return "BinaryField"
    def to_python(self, value):
        if isinstance(value,bytes):
            return value
        if isinstance(value, str):
            url(value)
            return Encrypter(value)
        return Encrypter(str(value))

    def get_prep_value(self, value):
        return self.to_python(value)
    
    def from_db_value(self, value, expression, connection):
        if value is not None:
            return str(Decrypter(value).decode())
        else:
            return None
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.to_python(value)

