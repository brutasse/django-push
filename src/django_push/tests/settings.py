DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'push.sqlite3',
        'TEST_NAME': ':memory:',
    },
}

INSTALLED_APPS = [
    'django.contrib.sites',
    'django_push.subscriber',
    'django_push.tests.pub',
    'django_push.tests.sub',
    'django_push.tests.hub',
]

ROOT_URLCONF = 'django_push.tests.urls'

SITE_ID = 1

PUSH_HUB = 'http://testserver/hub/'
PUSH_HUB = 'http://pubsubhubbub.appspot.com'
