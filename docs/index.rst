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

* Subscribers are feed readers. When the fetch a feed, they notice a hub is
  declared and subscribe to the feed's update with the hub.

* Hubs fetches the published feed when it gets a ping from the publicher and
  takes care of notifying all the subscribers.

.. _PubSubHubbub: http://code.google.com/p/pubsubhubbub/

This library provides hooks to add PubSubHubbub support to your Django
project: you can use it to be a publisher, a subscriber, a hub or all three.

.. toctree::
   :maxdepth: 2

   publisher
   subscriber
   hub

