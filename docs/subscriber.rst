Being a subscriber
==================

* Add ``django_push.subscriber`` to your ``INSTALLED_APPS`` and
  run ``manage.py syncdb``

* Include ``django_push.subscriber.urls`` in your main urlconf:

  .. code-block:: python

      urlpatterns = patterns('',
          # ...
          url(r'^subscriber/', include('django_push.subscriber.urls')),
      )

* Make sure the Sites framework is correctly configured.

Initial subscription
--------------------

Let's assume you're already parsing feeds. Your code may look like this:

.. code-block:: python

    import feedparser


    parsed = feedparser.parse('http://example.com/feed/')
    for entry in parsed.entries:
        # Do something with the entries: store them, email them...
        do_something()

You need to modify this code to check if the feed declares a hub and initiate
a subscription for this feed.

.. code-block:: python

    parsed = feedparser.parse('http://example.com/feed/')

    if 'links' in parsed.feed:
        for link in parsed.feed.links:
            if link.rel == 'hub':
                # Hub detected!
                hub = link.href

Now that you found a hub, you can create a subscription:

.. code-block:: python

    from django_push.subscriber.models import Subscription


    subscription = Subscription.objects.subscribe(feed_url, hub=hub)

``subscribe()`` takes the feed URL as a required argument. If the hub is not
provided, the subscription manager will fetch the feed again to find the hub.

If a subscription for this feed already exists, no new subscription will be
created and the existing subscription will be renewed.

``subscribe()`` also takes an optional ``lease_seconds`` keyword argument. By
default, it is set to ``None`` and it's up to the hub to decide when the lease
expires. However, if you provide it, the hub may give you a lease for the
amount of time you asked.

If you want to set a default ``lease_seconds``, you can use the
``PUSH_LEASE_SECONDS`` setting.

Renewing the leases
-------------------

As we can see, the hub subscription can be valid for a certain amount of time.
Before they actually expire, hubs must send subscription requests to recheck
with subscribers if the subscription is still valid. Thus **subscriptions will
be renewed automatically**.

However, you can always renew the leases manually before the expire to make
sure they are not forgotten by the hub. For instance, this could be run once
a day:

.. code-block:: python

    import datetime

    from django_push.subscriber.models import Subscription


    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    for subscription in Subscription.objects.filter(verified=True):
        if subscription.lease_expiration is None:
            continue

        if subscription.lease_expiration < tomorrow:
            renewed = Subscription.objects.subscribe(subscription.topic,
                                                     subscription.hub)

Unsubscribing
-------------

If you want to stop receiving notification for a feed's updates, you need to
unsubscribe. This is as simple as doing:

.. code-block:: python

    from django_push.subscriber import Subscription


    Subscription.objects.unsubscribe('http://example.com/feed')

The hub is notified to cancel the subscription and the Subscription object is
deleted. You can also specify the hub if you want to:

.. code-block:: python

    Subscription.objects.unsubscribe(feed_url, hub=hub_url)

If you don't provide the ``hub`` keyword argument, the feed is fetched to find
the hub URL. However specifying the hub may be useful if the feed has several
hubs.

Authentication
--------------

Some hubs may require basic auth for subscription requests. Django-PuSH
provides a way to supply authentication information via a callable that takes
the hub URL as a parameter and returns None (no authentication required) or a
(username, password) tuple. For instance:

.. code-block:: python

    def custom_hub_credentials(hub_url):
        if hub_url == 'http://superfeedr.com/hubbub':
            return ('my_superfeedr_username', 'password')

And then, set the ``PUSH_CREDENTIALS`` setting to your custom function:

.. code-block:: python

    PUSH_CREDENTIALS = 'path.to.custom_hub_credentials'

This way you have full control of the way credentials are stored (database,
settings, filesystem…)

Listening to Hubs' notifications
--------------------------------

Once subscriptions are setup, the hubs will start to send notifications to
your callback URLs. Each time a notification is received, the
``django_push.subscriber.signals.updated`` signal is sent. You can define a
receiver function:

.. code-block:: python

    from django_push.subscriber.signals import updated


    def listener(notification, **kwargs):
        for entry in notification.entries:
            print entry.title, entry.link

    updated.connect(listener)

The ``notification`` parameter is a feedparser-parsed feed containing what's
changed. You can then save the new entries or do whatever you want in the
receiver function. Here is an example of the structure of ``notification``,
this comes directly from the `universal feedparser`_:

.. _universal feedparser: http://www.feedparser.org/

.. code-block:: python

    {'bozo': 0,
     'encoding': 'utf-8',
     'entries': [{'id': u'http://example.com/some-url',
                  'link': u'http://example.com/some-url',
                  'links': [{'href': u'http://example.com/some-url',
                             'rel': u'alternate',
                             'type': 'text/html'}],
                  'summary': u'test',
                  'summary_detail': {'base': '',
                                     'language': u'en-us',
                                     'type': 'text/html',
                                     'value': u'This is the content'},
                  'title': u'test',
                  'title_detail': {'base': '',
                                   'language': u'en-us',
                                   'type': 'text/plain',
                                   'value': u'This is the title'},
                  'updated': u'2010-07-05T16:28:35-05:00',
                  'updated_parsed': time.struct_time(tm_year=2010, tm_mon=7, tm_mday=5, tm_hour=21, tm_min=28, tm_sec=35, tm_wday=0, tm_yday=186, tm_isdst=0)}],
     'feed': {'id': u'http://example.com/updates/',
              'language': u'en-us',
              'link': u'http://example.com/updates/',
              'links': [{'href': u'http://example.com/updates/',
                         'rel': u'alternate',
                         'type': 'text/html'},
                        {'href': u'http://example.com/pub/feed/',
                         'rel': u'self',
                         'type': 'text/html'},
                        {'href': u'http://pubsubhubbub.appspot.com',
                         'rel': u'hub',
                         'type': 'text/html'}],
              'title': u'Latest entries',
              'title_detail': {'base': '',
                               'language': u'en-us',
                               'type': 'text/plain',
                               'value': u'Latest entries'},
              'updated': u'2010-08-11T13:47:53-05:00',
              'updated_parsed': time.struct_time(tm_year=2010, tm_mon=8, tm_mday=11, tm_hour=18, tm_min=47, tm_sec=53, tm_wday=2, tm_yday=223, tm_isdst=0)},
     'namespaces': {'': u'http://www.w3.org/2005/Atom'},
     'version': 'atom10'}

A more detailed example
-----------------------

For a more detailed example, let's say we have an ``Entry`` and a ``Feed``
model:

.. code-block:: python

    from django.db import models


    class Feed(models.Model):
        url = models.URLField()
        # ... and some extra fields

    class Entry(models.Model):
        feed = models.ForeignKey(Feed)
        title = models.CharField(max_length=255)
        link = models.URLField()
        timestamp = models.DateTimeField()
        summary = models.TextField()

Then we can define a receiver function this way:

.. code-block:: python

    def pubsubhubbub_update(notification, **kwargs):
        parsed = notification
        entries = []
        for entry in parsed.entries:
            e = Entry(title=entry.title)
            if 'description' in entry:
                e.summary = entry.description
            if 'summary' in entry:
                e.summary = entry.summary

            e.link = entry.link
            e.date = datetime.datetime(*entry.updated_parsed[:6])
            entries.append(e)

        for link in parsed.feed.links:
            if link['rel'] == 'self':
                url = link['href']

        for feed in Feed.objects.filter(url=url):
            for entry in entries:
                entry.id = None
                entry.feed = feed
                entry.save(force_insert=True)

Each time the callback URL is called, new entries are added to all feeds. Such
a behaviour can be useful if you're running a multi-user feed reader.
