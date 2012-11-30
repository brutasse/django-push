Django-PuSH
===========

PuSH is the other name of `PubSubHubbub`_, a publish/subscribe protocol based
on HTTP and allowing near-instant notifications of topic updates.

* Publishers are entities that publish their updates via HTTP resources. When a
  resource is updated with a new entry, they ping their *hub* saying they have
  some new content. The hub is also declared in the resource.

* Subscribers are feed readers or followers. When they fetch a resource, they
  notice a hub is declared and subscribe to the resource's updates with the
  hub.

* Hubs fetch the published resource when it gets a ping from the publisher and
  takes care of notifying all the subscribers.

.. _PubSubHubbub: http://code.google.com/p/pubsubhubbub/

This library provides hooks to add PubSubHubbub support to your Django
project: you can use it to be a publisher, a subscriber, a hub or all three.

The PubSubHubbub spec was initially designed for Atom feeds. The `0.3
version`_ of the spec defines resources as feeds. The `0.4`_ version allows
arbitrary content types. This app currently implements the spec in version 0.3
but support for 0.4 may be added in future releases.

.. _0.3: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html

.. _0.4: http://superfeedr-misc.s3.amazonaws.com/pubsubhubbub-core-0.4.html

Installation
------------

.. code-block:: bash

    pip install django-push

This should also install ``feedparser`` if you don't have it already.

Manual
------

.. toctree::
   :maxdepth: 2

   publisher
   subscriber
   hub

Changelog
---------

* 0.3 - 2010-08-18: subscribers can unsubscribe.
* 0.2 - 2010-08-12: signature handling of content distribution requests.
* 0.1 - 2010-08-11: initial release.

Upgrading
---------

If you're using ``django_push.subscriber`` 0.1 and you need to upgrade to 0.2
or higher, here is what you need to do:

* Run the following SQL query to add the ``secret`` column:

  .. code-block:: sql

    ALTER TABLE subscriber_subscription ADD secret varchar(255);

* If you want your subscriptions to use the `authenticated content
  distribution`_ mechanism, you need to re-subscribe to all your existing
  subscriptions.

.. _authenticated content distribution: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html#authednotify

Other projects
--------------

* `SubHub`_ is a personal hub for your own feeds, although it's not completely
  real-time.

.. _SubHub: https://launchpad.net/subhub

* `djpubsubhubbub`_ implements the subscriber part of PubSubHubbub.

.. _djpubsubhubbub: https://git.participatoryculture.org/djpubsubhubbub/

* `PubSubHubbub_Publisher`_ is a publisher client for Python.

.. _PubSubHubbub_Publisher: http://pypi.python.org/pypi/PubSubHubbub_Publisher/1.0
