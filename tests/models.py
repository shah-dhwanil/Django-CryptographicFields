from django.db import models
from CryptographicFields.fields import *

class Character(models.Model):
    char=CharField(max_length=120)
    email=EmailField()
    text=TextField()
    slug=SlugField()
    ip=GenericIPAddressField()
    url=URLField()
    file=FilePathField(path="test/")

class Numeric(models.Model):
    bigint=BigIntegerField()
    smallint=SmallIntegerField()
    float=FloatField()
    decimal=DecimalField(max_digits=10,decimal_places=2)
    int=IntegerField()
    positivebigint=PositiveBigIntegerField()
    positiveint=PositiveIntegerField()
    positivesmallint=PositiveSmallIntegerField()

class Uuid(models.Model):
    uuid=UUIDField()
class Binary(models.Model):
    binary=BinaryField()
class Boolean(models.Model):
    boolean=BooleanField()

class DateTime(models.Model):
    date=DateField()
    time=TimeField()
    datetime=DateTimeField()