import mock

from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from django_push import UA
from django_push.publisher import ping_hub
from django_push.publisher.feeds import Feed


class PubTestCase(TestCase):
    @mock.patch('requests.post')
    def test_explicit_ping(self, post):
        post.return_value = 'Response'
        with self.assertRaises(ValueError):
            ping_hub('http://example.com/feed')

        response = ping_hub('http://example.com/feed',
                            hub_url='http://example.com/hub')
        post.assert_called_once_with(
            'http://example.com/hub',
            headers={'User-Agent': UA},
            data={'hub.url': 'http://example.com/feed',
                  'hub.mode': 'publish'})

    @mock.patch('requests.post')
    @override_settings(PUSH_HUB='http://hub.example.com')
    def test_ping_settings(self, post):
        post.return_value = 'Response'
        response = ping_hub('http://example.com/feed')
        post.assert_called_once_with(
            'http://hub.example.com',
            headers={'User-Agent': UA},
            data={'hub.url': 'http://example.com/feed',
                  'hub.mode': 'publish'})

    @mock.patch('requests.post')
    @override_settings(PUSH_HUB='http://hub.example.com')
    def test_ping_settings_override(self, post):
        post.return_value = 'Response'
        response = ping_hub('http://example.com/feed',
                            hub_url='http://google.com')
        post.assert_called_once_with(
            'http://google.com',
            headers={'User-Agent': UA},
            data={'hub.url': 'http://example.com/feed',
                  'hub.mode': 'publish'})

    @override_settings(PUSH_HUB='http://hub.example.com')
    def test_hub_declaration(self):
        class HubFeed(Feed):
            link = '/feed/'

            def items(self):
                return [1, 2, 3]

            def item_title(self, item):
                return str(item)

            def item_link(self, item):
                return '/items/{0}'.format(item)

        request = RequestFactory().get('/feed/')
        response = HubFeed()(request)
        hub_declaration = response.content.split('</updated>',
                                                 1)[1].split('<entry>', 1)[0]
        self.assertEqual(len(hub_declaration), 53)
        self.assertTrue('rel="hub"' in hub_declaration)
        self.assertTrue('href="http://hub.example.com' in hub_declaration)

        class OverrideHubFeed(HubFeed):
            hub = 'http://example.com/overridden-hub'

        request = RequestFactory().get('/feed/')
        response = OverrideHubFeed()(request)
        hub_declaration = response.content.split('</updated>',
                                                 1)[1].split('<entry>', 1)[0]
        self.assertEqual(len(hub_declaration), 64)
        self.assertTrue('rel="hub"' in hub_declaration)
        self.assertFalse('href="http://hub.example.com' in hub_declaration)
        self.assertTrue(
            'href="http://example.com/overridden-hub' in hub_declaration
        )

        class DynamicHubFeed(HubFeed):
            def get_hub(self, obj):
                return 'http://dynamic-hub.example.com/'

        request = RequestFactory().get('/feed/')
        response = DynamicHubFeed()(request)
        hub_declaration = response.content.split('</updated>',
                                                 1)[1].split('<entry>', 1)[0]
        self.assertEqual(len(hub_declaration), 62)
        self.assertTrue('rel="hub"' in hub_declaration)
        self.assertFalse('href="http://hub.example.com' in hub_declaration)
        self.assertTrue(
            'href="http://dynamic-hub.example.com/' in hub_declaration
        )
