# Django-CryptographicFields
A Django app for using cryptography in Django Models. It support bi-directional cryptography.

Check out the documentation  :- [Django-CryptographicFields](https://django-cryptographicfields.readthedocs.io/en/latest/)

# Requirements
* Python (3.6+)
* Pycryptodome (3.9+)
* Django (3.0+)
* Timestring (1.6.0+) Mandatory if python < 3.7
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
CRYPTOGRAPHIC_KEY="your_key"
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
3. **_Supports Ordering data through python functions_**
3. **_Supports Sorting data through python functions_**
4. **_Supports 'startswith' lookups for all String Based Fields_**
5. **_Supports 'date' lookup for Date,DateTime Fields_**
6. **_Supports 'time' lookup for TimeField_**

For More Information check out the documentation :- [Django-CryptographicFields](https://django-cryptographicfields.readthedocs.io/en/latest/)
