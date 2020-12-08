Examples
========

Cryptography by example
-----------------------

Using symmetrical encryption to store sensitive data in the database.

.. code-block:: python

   from django.db import models

   from CryptographicFields.fields import *


   class User(models.Model):
        uuid = UUIDField()
        username = CharField(max_length=20)
        first_name = CharField(max_length=120)
        last_name = CharField(max_length=120)
        age = SmallIntegerField()
        email = EmailField()
        joined = DateTimeField()

The data will now be automatically encrypted when saved to the
database & decrypted when retrived with django's ORM.CryptographicFields uses an encryption that allows for bi-directional data retrieval.

Generating Data

.. code-block:: python

    from .models import User
    from uuid import uuid5,NAMESPACE_URL
    import datetime

    User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.a.random.com"), username="admin", first_name="Albert",
                                         last_name="Frost", age=24, email="albert@gmail.com", joined=datetime.datetime(2015, 12, 26, 18, 35, 54))
    User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.b.random.com"), username="empi16", first_name="Empi",
                                         last_name="Tsar", age=16, email="empi@rediff.com", joined=datetime.datetime(2025, 12, 28, 12, 35, 34))
    User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.c.random.com"), username="dextEr", first_name="Dexter",
                                         last_name="Flutnes", age=28, email="dextEr@random.com", joined=datetime.datetime(2018, 2, 20, 20, 50, 15))
    User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.d.random.com"), username="shahprogrammer", first_name="Dhwanil",
                                         last_name="Shah", age=18, email="shahprogrammer@random.com", joined=datetime.datetime(2018, 4, 1, 20, 25, 14))
    User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.e.random.com"), username="graphin", first_name="Graphin",
                                         last_name="frost", age=30, email="graphin@yahoo.com", joined=datetime.datetime(2005, 9, 22, 9, 33, 40))
    User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.f.random.com"), username="abc", first_name="abc",
                                         last_name="xyz", age=16, email="abc@yahoo.com", joined=datetime.datetime(2009, 7, 22, 14, 5, 40))

Sorting by example
--------------------
.. code-block:: python

    from .models import User
    from CryptographicFields.filters import sort,iendswith,startswith

    # You can use any method that generate QuerySet object like all,filters etc
    queryset=User.objects.all()
    """Sort function takes first arg Queryset second sort_function third field name 
    fourth your query value & return new QuerySet object with sorted data"""
    # using iendswith to sort queryset
    sort_queryset=sort(queryset, iendswith, 'username', "er")
    print(sort_queryset)
    <QuerySet [<User: User object (3)>, <User: User object (4)>]>
    # using startswith to sort queryset
    sort_queryset=sort(self.queryset, startswith, 'last_name', "F")
    print(sort_queryset)
    <QuerySet [<User: User object (1)>, <User: User object (3)>]>

Ordering by example
-------------------
.. code-block:: python

    from .models import User
    from CryptographicFields.filters import order_by

    # You can use any method that generate QuerySet object like all,filters etc
    queryset=User.objects.all()
    """Order_by functions takes queryset as first arg & 
    tuple with fields_name from higher priority to lower priority
    For eg in this case highest priority is age & lowest priority is username.
    i.e it will sort queryset with username field value if it finds two or more objects with same age value"""
    # Ascending Order
    order_queryset=(order_by(self.queryset, ("age", "username"))
    print(order_queryset)
    <QuerySet [<User: User object (6)>, <User: User object (2)>,
     <User: User object (4)>, <User: User object (1)>,
     <User: User object (3)>, <User: User object (5)>]>
    # Descending Order
    order_queryset=(order_by(self.queryset, ("age", "username"),reverse=True)
    print(order_queryset)
    <QuerySet [<User: User object (5)>, <User: User object (3)>,
     <User: User object (1)>, <User: User object (4)>, 
     <User: User object (2)>, <User: User object (6)>]>