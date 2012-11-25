import os
import sys

from django.conf import settings

try:
    from django.utils.functional import empty
except ImportError:
    empty = None


def setup_test_environment():
    # reset settings
    settings._wrapped = empty

    apps = [
        'tests.publisher',
    ]

    settings_dict = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    'push.sqlite',
                ),
            },
        },
        'INSTALLED_APPS': apps,
        'STATIC_URL': '/static/',
        'SECRET_KEY': 'test secret key',
    }

    settings.configure(**settings_dict)


def runtests(*test_args):
    setup_test_environment()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=1, interactive=True,
                                   failfast=False)
    failures = runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
