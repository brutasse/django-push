Being a publisher
=================

Declare your hub
----------------

First, you need a hub. You can either use your own (see :ref:`hub`) or use a
`public hub`_. See the hub's documentation for adding a new feed and add your
hub's URL as a ``PUSH_HUB`` setting (the URL **must** be a full URL):

.. _public hub: https://pubsubhubbub.appspot.com

.. code-block:: python

    PUSH_HUB = 'https://pubsubhubbub.appspot.com'

Finally, use *django-push*'s base feed to declare your feeds. Instead of
importing ``django.contrib.syndication.views.Feed``, do it this way:

.. code-block:: python

    from django_push.publisher.feeds import Feed


    class MyFeed(Feed):
        title = 'My Feed'
        link = '...'

        def items(self):
            return MyModel.objects.filter(...)

Django-push will take care of adding the hub declaration to the feeds. By
default, the hub is set to your ``PUSH_HUB`` setting. If you want to change
it, see :ref:`different-hubs`.

Django-push's feed is just a slightly modified version of the ``Feed`` class
from the ``contrib.syndication`` app, however its type is forced to be an
Atom feed. While some hubs may be compatible with RSS and Atom feeds, the
PubSubHubbub specifications encourages the use of Atom feeds. Make sure you
use the Atom attributes, like ``subtitle`` instead of ``description`` for
instance. If you're already publishing Atom feeds, you're fine.

.. _different-hubs:

Use different hubs for each feed
````````````````````````````````

If you want to use different hubs for different feeds, just set the ``hub``
attribute to the URL you want:

.. code-block:: python

    from django_push.publisher.feeds import Feed


    class MyFeed(Feed):
        title = 'My Feed'
        link = '...'
        hub = 'http://hub.example.com'


    class MyOtherFeed(Feed):
        hub = 'http://some-other-hub.com'

By default, the ``Feed`` class will use the ``PUSH_HUB`` setting.

Ping the hub on feed updates
----------------------------

Once your feeds are configured, you need to ping the hub each time a new
item/entry is published. Since you may have your own publishing mechanics, you
need to call a ``ping_hub`` function when a new entry is made available. For
example, if a model has a ``publish()`` method:

.. code-block:: python

    from django.contrib.sites.models import Site
    from django.db import models

    from django_push.publisher import ping_hub


    class MyModel(models.Model):

        def publish(self):
            self.published = True
            self.timestamp = datetime.datetime.utcnow()
            self.save()

            ping_hub('http://%s%s' % (Site.objects.get_current(),
                                      self.get_absolute_url()))

``ping_hub`` has to be called with a full URL as parameter, using either the
Sites framework or your own mechanism. By default, ``ping_hub`` will ping the
hub declared in the ``PUSH_HUB`` setting. A different hub can set using an
optional ``hub_url`` keyword argument:

.. code-block:: python

    from django_push.publisher import ping_hub


    ping_hub('http://example.com/feed.atom',
             hub_url='http://hub.example.com')
