Django-PuSH
===========

.. image:: https://travis-ci.org/brutasse/django-push.png?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/brutasse/django-push

PubSubHubbub support for Django.

* Author: Bruno Renié and `contributors`_
* Licence: BSD

.. _contributors: https://github.com/brutasse/django-push/contributors

Usage
-----

The documentation is `available on ReadTheDocs`_.

.. _available on ReadTheDocs: https://django-push.readthedocs.org/

Contributing
------------

Links to the PubSubHubbub specs: `0.4`_, `0.3`_.

.. _0.4: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.4.html
.. _0.3: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html

* The project is on github: https://github.com/brutasse/django-push
* To setup a development environment, run::

      mkvirtualenv django-push
      pip install -r requirements-dev.txt Django

  Then run the tests::

      python setup.py test

Use ``tox`` to run the tests across all supported Python / Django version
combinations::

    pip install tox
    tox

To get code coverage stats::

    pip install coverage
    coverage run runtests.py
    coverage html
    open htmlcov/index.html
