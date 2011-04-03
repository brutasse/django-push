import urllib2
import feedparser
from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.test import TestCase

from django_push.subscriber.models import Subscription
from django_push.subscriber.signals import updated


def mock_open(request):
    raise urllib2.HTTPError('request', 204, 'no-op', {}, StringIO(''))

urllib2.Request = lambda x, y, z: 'request'
urllib2.urlopen = mock_open


class SubTest(TestCase):

    def signal_handler(self, notification, **kwargs):
        self.signals.append(notification)

    def setUp(self):
        self.subscription = Subscription.objects.create(
            hub='http://testhub.example.com', topic='http://example.com/foo',
            verified=True, verify_token='blah')
        self.signals = []
        updated.connect(self.signal_handler)

    def test_callback_invalid_feed_data(self):
        """Ignore posts that contain invalid feed data in the raw post data."""
        url = reverse('subscriber_callback', args=[self.subscription.pk])
        response = self.client.post(url, 'foobar',
                                    content_type='application/atom+xml')
        self.assertEquals(response.status_code, 200)

    def test_callback_valid_feed_data(self):
        feed_data = """<?xml version='1.0'?>
        <feed xmlns='http://www.w3.org/2005/Atom' xml:lang='en-US'>
            <link type='text/html' rel='alternate' href='http://example.com/'/>
            <link type='application/atom+xml' rel='self'
                href='http://example.com/feed/'/>
            <entry>

            </entry>
        </feed>
        """
        parsed = feedparser.parse(feed_data)
        url = reverse('subscriber_callback', args=[self.subscription.pk])
        response = self.client.post(url, feed_data,
                                    content_type='application/atom+xml')

        # verify that we get a 200 and parsed as xml sent as a signal
        self.assertEquals(response.status_code, 200)
        last_signal = self.signals.pop()
        self.assertTrue(parsed == last_signal)
