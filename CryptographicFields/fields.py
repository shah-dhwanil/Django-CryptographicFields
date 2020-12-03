from typing import Any
from django.db import models
from django.core import exceptions, validators
from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from .cryptography import encrypt, decrypt
from ast import literal_eval
import datetime
from django import forms
from django.utils import timezone
from timestring import Date
from decimal import Decimal
from uuid import UUID
from django.utils.translation import gettext_lazy as _
from django.db.models.lookups import StartsWith as StartWith, FieldGetDbPrepValueMixin
"""
to_python() make validations & checks type of the data
get_db_prep_value() encrypts the data
from_db_value() decrypts the data returned from the db
pre_save() generates date ,datetime,time for the respestive fields
get_db_prep_save() saves the value into db
"""


class StartsWith(FieldGetDbPrepValueMixin, StartWith):
    pass


class CharField(models.CharField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return decrypt(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class BooleanField(models.BooleanField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return literal_eval(decrypt(value))

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class DateField(models.DateField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(connection.ops.adapt_datefield_value(value))

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return datetime.date.fromisoformat(decrypt(value))

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = datetime.date.today()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class DateTimeField(models.DateTimeField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return super().get_prep_value(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(connection.ops.adapt_datetimefield_value(value))

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return datetime.datetime.fromisoformat(decrypt(value))

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = timezone.now()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class TimeField(models.TimeField):

    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts dates into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(connection.ops.adapt_timefield_value(value))

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return datetime.time.fromisoformat(decrypt(value))

    def pre_save(self, model_instance, add):
        if self.auto_now or (self.auto_now_add and add):
            value = datetime.datetime.now().time()
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class DecimalField(models.DecimalField):

    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return super().to_python(value)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def get_db_prep_save(self, value, connection,):
        return encrypt(connection.ops.adapt_decimalfield_value(self.get_prep_value(value), self.max_digits, self.decimal_places))

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return float(decrypt(value))
        # return value

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class EmailField(CharField):
    default_validators = [validators.validate_email]
    description = _("Email address")

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs.setdefault('max_length', 254)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # As with CharField, this will cause email validation to be performed
        # twice.
        return super().formfield(**{
            'form_class': forms.EmailField,
            **kwargs,
        })


class FloatField(models.FloatField):

    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return float(decrypt(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class IntegerField(models.IntegerField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return int(decrypt(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class BigIntegerField(IntegerField):
    error_messages = {
        'invalid': _('“%(value)s” value must be less than %(max) & greater than %(min).'),
    }
    description = _("Big (8 byte) integer")
    MAX_BIGINT = 9223372036854775807

    def to_python(self, value: Any) -> Any:
        value = self.clean(super().to_python(value), None)
        if value < (-self.MAX_BIGINT-1) or value > self.MAX_BIGINT:
            raise exceptions.ValidationError(self.error_messages['invalid'], code='invalid',
                                             params={'value': value, 'max': self.MAX_BIGINT, 'min': (-self.MAX_BIGINT-1)})
        return value

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': -self.MAX_BIGINT - 1,
            'max_value': self.MAX_BIGINT,
            **kwargs,
        })


class GenericIPAddressField(models.GenericIPAddressField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(connection.ops.adapt_ipaddressfield_value(value))

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return decrypt(value)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class PositiveBigIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField):
    description = _('Positive big integer')

    error_messages = {
        'invalid': _('“%(value)s” value must be less than greater than %(min).'),
    }

    def to_python(self, value: Any) -> Any:
        value = self.clean(super().to_python(value), None)
        if value < 0:
            raise exceptions.ValidationError(self.error_messages['invalid'], code='invalid',
                                             params={'value': value, 'min': 0})
        return value

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })


class PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField):
    description = _("Positive integer")
    error_messages = {
        'invalid': _('“%(value)s” value must be less than greater than %(min).'),
    }

    def to_python(self, value: Any) -> Any:
        value = self.clean(super().to_python(value), None)
        if value < 0:
            raise exceptions.ValidationError(self.error_messages['invalid'], code='invalid',
                                             params={'value': value, 'min': 0})
        return value

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })


class PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField):
    description = _("Positive small integer")

    error_messages = {
        'invalid': _('“%(value)s” value must be less than greater than %(min).'),
    }

    def to_python(self, value: Any) -> Any:
        value = self.clean(super().to_python(value), None)
        if value < 0:
            raise exceptions.ValidationError(self.error_messages['invalid'], code='invalid',
                                             params={'value': value, 'min': 0})
        return value

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })


class SlugField(CharField):

    default_validators = [validators.validate_slug]
    description = _("Slug (up to %(max_length)s)")

    def __init__(self, *args, max_length=50, db_index=True, allow_unicode=False, **kwargs):
        self.allow_unicode = allow_unicode
        if self.allow_unicode:
            self.default_validators = [validators.validate_unicode_slug]
        super().__init__(*args, max_length=max_length, db_index=db_index, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 50:
            del kwargs['max_length']
        if self.db_index is False:
            kwargs['db_index'] = False
        else:
            del kwargs['db_index']
        if self.allow_unicode is not False:
            kwargs['allow_unicode'] = self.allow_unicode
        return name, path, args, kwargs

    def get_internal_type(self):
        return "SlugField"

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.SlugField,
            'allow_unicode': self.allow_unicode,
            **kwargs,
        })


class SmallIntegerField(IntegerField):
    description = _("Small integer")


class TextField(models.TextField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return decrypt(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class URLField(CharField):
    default_validators = [validators.URLValidator()]
    description = _("URL")

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs.setdefault('max_length', 200)
        super().__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get("max_length") == 200:
            del kwargs['max_length']
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        return super().formfield(**{
            'form_class': forms.URLField,
            **kwargs,
        })


class BinaryField(models.BinaryField):

    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        if isinstance(value, str):
            value = bytes(value, "UTF-8")
        elif isinstance(value, memoryview):
            value = bytes(value)
        value = self.clean(value, None)
        return value

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return bytes.fromhex(decrypt(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(bytes(connection.Database.Binary(value)).hex())

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class UUIDField(models.UUIDField):

    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        
        return UUID(hex=decrypt(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value.hex)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


class FilePathField(models.FilePathField):
    def get_internal_type(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Any:
        return self.clean(super().to_python(value), None)

    def get_prep_value(self, value: Any) -> Any:
        return self.to_python(value)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        return decrypt(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return encrypt(value)
    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python() and validate() are propagated. Return the correct
        value if no error is raised.
        """
        self.validate(value, model_instance)
        self.run_validators(value)
        return value


CharField.register_lookup(StartsWith)
BooleanField.register_lookup(StartsWith)
DateField.register_lookup(StartsWith)
DateTimeField.register_lookup(StartsWith)
EmailField.register_lookup(StartsWith)
GenericIPAddressField.register_lookup(StartsWith)
SlugField.register_lookup(StartsWith)
TextField.register_lookup(StartsWith)
URLField.register_lookup(StartsWith)
BinaryField.register_lookup(StartsWith)
UUIDField.register_lookup(StartsWith)
FilePathField.register_lookup(StartsWith)
DateField.register_lookup(StartsWith, lookup_name="date")
DateTimeField.register_lookup(StartsWith, lookup_name="date")
TimeField.register_lookup(StartsWith, lookup_name="time")
