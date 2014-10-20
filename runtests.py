import os
import sys
import warnings

warnings.simplefilter('always')

import django

from django.conf import settings
from django.utils.functional import empty


def runtests(*test_args):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    if django.VERSION >= (1, 7):
        django.setup()

    from django.test.simple import DjangoTestSuiteRunner
    runner = DjangoTestSuiteRunner(verbosity=1, interactive=True,
                                   failfast=False)
    failures = runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
