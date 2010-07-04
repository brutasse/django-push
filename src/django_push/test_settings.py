DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'push.sqlite3',
        'TEST_NAME': ':memory:',
    },
}

INSTALLED_APPS = [
    'django.contrib.sites',
    'django_push',
    'django_push.subscriber',
]

ROOT_URLCONF = 'django_push.urls'

SITE_ID = 1
