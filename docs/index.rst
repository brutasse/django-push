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
project: you can use it to be a publisher and/or subscriber.

The PubSubHubbub spec was initially designed for Atom feeds. The `0.3
version`_ of the spec defines resources as feeds. The `0.4`_ version allows
arbitrary content types. The `0.4`_ spec is supported since version **0.5** of
django-push. We unfortunately missed the chance of having version numbers
match properly.

.. _0.3 version: http://pubsubhubbub.googlecode.com/svn/trunk/pubsubhubbub-core-0.3.html

.. _0.4: http://superfeedr-misc.s3.amazonaws.com/pubsubhubbub-core-0.4.html

Installation
------------

.. code-block:: bash

    pip install django-push

Manual
------

.. toctree::
   :maxdepth: 2

   publisher
   subscriber

Changelog
---------

* **0.5**:

  * Python 3 support, Django >= 1.4.1 support.

  * HTTP handling via requests instead of urllib2.

  * Deprecation of ``Subscription.objects.unsubscribe()`` in favor of an
    instance method on the subscription object. The ``unsubscribe()`` manager
    method will be removed in version 0.6.

  * ``Subscription.objects.subscribe()`` raises a warning if the ``hub`` kwarg
    is not provided. It will become mandatory in version 0.6.

  * Removed ``hub.verify_token`` from subscription requests. It's optional in
    the 0.3 spec and absent from the 0.4 spec.

  * Secret generation code uses ``django.utils.crypto`` instead of the
    ``random`` module. In addition, subscriptions over HTTP don't use a secret
    anymore (as recommended in the spec).

  * The ``updated`` signal is sent with the raw payload instead of the result
    of a ``feedparser.parse`` call. This allows other content types than feeds
    to be processed, as suggested in version 0.4 of the PubSubHubbub spec.

  * The callback view is now a class-based view, allowing listening for content
    distribution via a custom view if the ``updated`` signal is not suitable.

  * ``django.contrib.sites`` is no longer a hard requirement. You can set
    ``PUSH_DOMAIN`` in your settings to your site's canonical hostname.

  * South migrations support. If you don't use South, you should. If you're
    upgrading from 0.4, just **fake the first migration** and apply the
    others::

        ./manage.py migrate subscriber 0001_initial --fake
        ./manage.py migrate

* **0.4** (2011-06-30):

  * Support for hub authentication via ``PUSH_HUB_CREDENTIALS``.

  * Support for SSL callback URLs.

* **0.3** (2010-08-18):

  * Subscribers can unsubscribe.

* **0.2** (2010-08-12):

  * Signature handling of content distribution requests.

* **0.1** (2010-08-11):

  * Initial release.
