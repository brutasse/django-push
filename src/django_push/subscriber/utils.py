import feedparser

from django.conf import settings
from django.utils.importlib import import_module


def get_hub(topic):
    parsed = feedparser.parse(topic)
    for link in parsed.feed.links:
        if link['rel'] == 'hub':
            return link['href']
    raise TypeError("Hub not found")


def hub_credentials(hub_url):
    """A callback that returns no credentials, for anonymous
    subscriptions. Meant to be overriden if developers need to
    authenticate with certain hubs"""
    return


def get_hub_credentials(hub_url):
    creds_path = getattr(settings, 'PUSH_CREDENTIALS',
                         'django_push.subscriber.utils.hub_credentials')
    creds_path, creds_function = creds_path.rsplit('.', 1)
    creds_module = import_module(creds_path)
    return getattr(creds_module, creds_function)(hub_url)
