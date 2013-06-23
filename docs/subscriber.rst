Being a subscriber
==================

* Add ``django_push.subscriber`` to your ``INSTALLED_APPS`` and
  run ``manage.py syncdb``. If you use South, run ``manage.py migrate``.

* Include ``django_push.subscriber.urls`` in your main urlconf:

  .. code-block:: python

      urlpatterns = patterns('',
          # ...
          url(r'^subscriber/', include('django_push.subscriber.urls')),
      )

* If you have ``django.contrib.sites`` installed, make sure it is correctly
  configured: check that ``Site.objects.get_current()`` actually returns the
  domain of your publicly accessible website.

* If you don't use ``django.contrib.sites``, set ``PUSH_DOMAIN`` to your
  site's domain in your settings.

* Additionally if your site is available via HTTPS, set ``PUSH_SSL_CALLBACK``
  to ``True``.

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


    subscription = Subscription.objects.subscribe(feed_url, hub=hub,
                                                  lease_seconds=12345)

If a subscription for this feed already exists, no new subscription is
created but the existing subscription is renewed.

``lease_seconds`` is optional and **only a hint** for the hub. If the hub has
a custom expiration policy it may chose another value arbitrarily. The value
chose by the hub is saved in the subscription object when the subscription
gets verified.

If you want to set a default ``lease_seconds``, you can use the
``PUSH_LEASE_SECONDS`` setting.

Renewing the leases
-------------------

As we can see, the hub subscription can be valid for a certain amount of time.

Version 0.3 of the PubSubHubbub spec explains that hub must recheck with
subscribers before subscriptions expire to automatically renew subscriptions.
This is not the case in version 0.4 of the spec.

In any case you can renew the leases before the expire to make sure they are
not forgotten by the hub. For instance, this could be run once a day:

.. code-block:: python

    import datetime

    from django.utils import timezone

    from django_push.subscriber.models import Subscription


    tomorrow = timezone.now() + datetime.timedelta(days=1)

    for subscription in Subscription.objects.filter(
        verified=True,
        lease_expiration__lte=tomorrow
    ):
        subscription.subscribe()

Unsubscribing
-------------

If you want to stop receiving notification for a feed's updates, you need to
unsubscribe. This is as simple as doing:

.. code-block:: python

    from django_push.subscriber.models import Subscription

    subscription = Subscription.objects.get(topic='http://example.com/feed')
    subscription.unsubscribe()

The hub is notified to cancel the subscription and the Subscription object is
deleted. You can also specify the hub if a topic uses several hubs:

.. code-block:: python

    subscription = Subscription.objects.get(topic=feed_url, hub=hub_url)
    subscription.unsubscribe()

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

And then, set the ``PUSH_CREDENTIALS`` setting to the dotted path to your
custom function:

.. code-block:: python

    PUSH_CREDENTIALS = 'path.to.custom_hub_credentials'

This way you have full control of the way credentials are stored (database,
settings, filesystem…)

Using HTTPS Callback URLs
-------------------------

By default, callback URLs will be constructed using HTTP. If you would like
to use HTTPS for callback URLs, set the ``PUSH_SSL_CALLBACK`` setting to True:

.. code-block:: python

    PUSH_SSL_CALLBACK = True

Listening to Hubs' notifications
--------------------------------

Once subscriptions are setup, the hubs will start to send notifications to
your callback URLs. Each time a notification is received, the
``django_push.subscriber.signals.updated`` signal is sent. You can define a
receiver function:

.. code-block:: python

    import feedparser

    from django_push.subscriber.signals import updated

    def listener(notification, **kwargs):
        parsed = feedparser.parse(notification)
        for entry in parsed.entries:
            print entry.title, entry.link

    updated.connect(listener)

The ``notification`` parameter is the raw payload from the hub. If you expect
an RSS/Atom feed you should process the payload using a library such as the
`universal feedparser`_.

.. _universal feedparser: http://pythonhosted.org/feedparser/

Listening with a view instead of the ``updated`` signal
-------------------------------------------------------

If Django signals are not your thing, you can inherit from the base subscriber
view to listen for notifications:

.. code-block:: python

    from django_push.subscriber.views import CallbackView

    class MyCallback(CallbackView):
        def handle_subscription(self):
            payload = self.request.body
            parsed = feedparser.parse(payload)
            for entry in payload.entries:
                do_stuff_with(entry)
    callback = MyCallback.as_view()

Then instead of including ``django_push.subscriber.urls`` in your urlconf,
define a custom URL with ``subscriber_callback`` as a name and a ``pk`` named
parameter:

.. code-block:: python

    from django.conf.urls import patterns, url

    from .views import callback

    urlpatterns = patterns(
        '',
        url(r'^subscriber/(?P<pk>\d+)/$', callback, name='subscriber_callback'),
    )

Logging
-------

You can listen for log messages by configuring the ``django_push`` logger:

.. code-block:: python

    LOGGING = {
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django_push': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
