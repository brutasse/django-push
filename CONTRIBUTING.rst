.. image:: https://jazzband.co/static/img/jazzband.svg
   :target: https://jazzband.co/
   :alt: Jazzband

This is a `Jazzband <https://jazzband.co>`_ project. By contributing you agree to abide by the `Contributor Code of Conduct <https://jazzband.co/about/conduct>`_ and follow the `guidelines <https://jazzband.co/about/guidelines>`_.

Development
-----------

You can contribute to this project forking it from GitHub and sending pull requests.

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

Useful Resources
----------------

Links to the PubSubHubbub specs: `0.4`_, `0.3`_.

.. _0.4: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.4.html
.. _0.3: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html