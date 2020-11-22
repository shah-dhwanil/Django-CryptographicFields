Settings
========

.. code-block :: py3

    INSTALLED_APPS = [
        ...
        'CryptographicFields',
    ]


:const:`ENCRYPTION_KEY`

Default: :obj:`None`

When value is :obj:`None` a key will be derived from
``SECRET_KEY``. Otherwise the value will be used for the key.
While specifiing key make sure that it must contain 50 letters otherwise it will raiser an error 
:py:exc:`CryptographicFields.utils.LengthError`