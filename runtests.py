import os
import sys
import warnings

import django
from django.test.runner import DiscoverRunner

warnings.simplefilter('always')


def runtests():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    django.setup()

    runner = DiscoverRunner(verbosity=1, interactive=True,
                            failfast=False)
    failures = runner.run_tests(())
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
