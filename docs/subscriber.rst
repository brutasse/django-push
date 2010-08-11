Being a subscriber
==================

First:

* You need to add ``django_push.subscriber`` to your ``INSTALLED_APPS`` and
  run ``manage.py syncdb``

* You need to include ``django_push.subscriber.urls`` in your main urlconf:

  .. code-block:: python

      urlpatterns = patterns('',
          # ...
          url(r'^subscriber/', include('django_push.subscriber.urls')),
      )

* You need to make sure the Sites framework is correctly configured.

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
Thus it is appropriate to renew the leases that will expire soon using a
management command. For instance, this could be run once a day:

.. code-block:: python

    import datetime

    from django_push.subscriber.models import Subscription

    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    for subscription in Subscription.objects.filter(verified=True):
        if subscription.lease_expiration < tomorrow:
            renewed = Subscription.objects.subscribe(subscription.topic,
                                                     subscription.hub)

This way you can renew you subscriptions before they completely expire.

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
receiver function.
