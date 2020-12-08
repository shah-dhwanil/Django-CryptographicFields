Settings
========

.. code-block :: py3

    INSTALLED_APPS = [
        ...
        'CryptographicFields',
    ]


:const:`CRYPTOGRAPHIC_KEY`

Default: :obj:`None`

When value of ``CRYPTOGRAPHIC_KEY`` is not :obj:`None` a key will be derived from
``CRYPTOGRAPHIC_KEY``. Otherwise the value will be used for the key will be from ``SECRET_KEY``.
While specifiing key make sure that it must contain 50 letters otherwise it will raise an error 
:py:exc:`CryptographicFields.cryptography.LengthError`