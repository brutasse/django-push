import urllib
import urllib2

from django.conf import settings


def ping_hub(feed_url, hub_url=None):
    if hub_url is None:
        hub_url = getattr(settings, 'PUSH_HUB')
        if hub_url is None:
            return
    params = {
        'hub.mode': 'publish',
        'hub.url': feed_url,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = urllib.urlencode(params)
    try:
        request = urllib2.Request(hub_url, data, headers)
        urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        if hasattr(e, 'code') and e.code == 204:
            return
        raise
