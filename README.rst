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
