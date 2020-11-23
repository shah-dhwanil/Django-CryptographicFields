# Django-CryptographicFields
A Django app for using cryptography in Django Models. It support bi-directional cryptography.
Check out the documentation :- [Django-CryptographicFields](https://django-cryptographicfields.readthedocs.io/en/latest/)
# Quick start
## 1.Install Django-CryptographicFields
Install Django CryptographicFields using PIP:-
```py
pip install Django-CryptographicFields
```
## 2. Add "CryptographicFields" to your INSTALLED_APPS setting like this:
``` py
    INSTALLED_APPS = [
        ...
        'CryptographicFields',
    ]
```
## 3.Custom Encryption Key
Set custom Encryption Key in settings.py
Make sure that key length is greater than or equal to 50 otherwise it will raise an error 
```py
ENCRYPTION_KEY="your_key"
```
# Creating Models using CryptographicFields

## Cryptography by example
```py
from CryptographicFields import fields
from django.db import models

class CryptogaphicModel(models.Model):
    name=fields.CharField(max_length=120)
```
The data will now be automatically encrypted when saved to the database.& decrypted when data is retrieved.

# Advantages over other projects:-
1. **_Supports data retrival_**
2. **_Supports custom query_**
3. **_Supports Q() queries_**
4. **_Supports 'startswith' lookups for all String Based Fields_**
5. **_Supports 'date' lookup for Date,DateTime Fields_**
6. **_Supports 'time' lookup for TimeField_**

# Requirements
* Python (3.6+)
* Pycryptodome (3.9+)
* Django (3.0+)
* Timestring(1.6.0+)
# List of Model Fields supported by CryptographicFields:
* ___BigIntegerField___
* ___BooleanField___
* ___BinaryField___
* ___CharField___
* ___DateField___
* ___DateTimeField___
* ___DecimalField___
* ___EmailField___
* ___FilePathField___
* ___FloatField___
* ___IntegerField___
* ___GenericIPAddressField___
* ___PositiveBigIntegerField___
* ___PositiveIntegerField___
* ___PositiveSmallIntegerField___
* ___SlugField___
* ___SmallIntegerField___
* ___TextField___
* ___URLField___
* ___UUIDField___
* ___TimeField___
