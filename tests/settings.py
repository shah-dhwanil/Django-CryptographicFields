SECRET_KEY = "test"
CRYPTOGRAPHIC_KEY=""
INSTALLED_APPS = [
    "tests",
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}