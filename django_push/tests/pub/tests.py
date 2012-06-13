import urllib2
from StringIO import StringIO

from django.test import TestCase

from django_push.tests.pub.models import Entry


def mock_request(url, data, headers):
    return 'request'


def mock_open(request):
    raise urllib2.HTTPError('request', 204, 'no-op', {}, StringIO(''))

urllib2.Request = mock_request
urllib2.urlopen = mock_open


class PubTest(TestCase):
    def test_hub(self):
        response = self.client.get('/pub/feed/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('rel="hub"' in response.content)

    def test_custom_hub(self):
        response = self.client.get('/pub/customfeed/')
        self.assertEquals(response.status_code, 200)
        self.assertTrue('http://myhub.com' in response.content)

    def test_publish(self):
        entry = Entry(title='My title',
                      content='My awesome content')
        entry.save()

        response = self.client.get('/pub/feed/')
        self.assertFalse('My title' in response.content)

        entry.publish()
