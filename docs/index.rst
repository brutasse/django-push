.. django-push documentation master file, created by
   sphinx-quickstart on Sun Jul  4 14:18:51 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django-PuSH
===========

PuSH is the other name of `PubSubHubbub`_, a publish/subscribe protocol based
on Atom and HTTP and allowing near-instant notifications of feed updates.

* Publishers are entities that publish their updates via Atom feeds. When a
  feed is updated with a new entry, they ping their *hub* saying they have
  some new content. The hub is also declared in the Atom feed.

* Subscribers are feed readers or aggregators. When the fetch a feed, they
  notice a hub is declared and subscribe to the feed's update with the hub.

* Hubs fetches the published feed when it gets a ping from the publisher and
  takes care of notifying all the subscribers.

.. _PubSubHubbub: http://code.google.com/p/pubsubhubbub/

This library provides hooks to add PubSubHubbub support to your Django
project: you can use it to be a publisher, a subscriber, a hub or all three
(actually, the hub isn't implemented yet but I'm sure you can help).

.. warning:: Django 1.2 only!

    **Django-PuSH** uses the new syndication framework from Django 1.2 as well
    as the ``csrf_exempt`` decorator. This makes it incompatible with older
    versions of Django.

    If you think this is a shame and you want to help, I'd be more than happy
    to `integrate your patches`_!

    .. _integrate your patches: http://github.com/brutasse/django-push

Installation
------------

.. code-block:: bash

    pip install -U django-push

Also make sure you have pip-installed ``feedparser``.

Manual
------

.. toctree::
   :maxdepth: 2

   publisher
   subscriber
   hub


Other projects
--------------

* `SubHub`_ is a personal hub for your own feeds, although it's not completely
  real-time.

.. _SubHub: https://launchpad.net/subhub

* `djpubsubhubbub`_ implements the subscriber part of PubSubHubbub.

.. _djpubsubhubbub: https://git.participatoryculture.org/djpubsubhubbub/

* `PubSubHubbub_Publisher`_ is a publisher client for Python.

.. _PubSubHubbub_Publisher: http://pypi.python.org/pypi/PubSubHubbub_Publisher/1.0
