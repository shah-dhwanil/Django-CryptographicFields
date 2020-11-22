Cryptography by example
=======================

Using symmetrical encryption to store sensitive data in the database.

.. code-block:: python

   from django.db import models

   from CryptographicFields.fields import CharField


   class MyModel(models.Model):
       name = models.CharField(max_length=50)
       sensitive_data = CharField(max_length=200)

The data will now be automatically encrypted when saved to the
database & decrypted when retrived with django's ORM.CryptographicFields uses an encryption that allows for bi-directional data retrieval.