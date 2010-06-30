import urllib
import urllib2


def ping_hub(hub_url, feed_url):
    params = {
        'hub.mode': 'publish',
        'hub.url': feed_url,
    }
    data = urllib.urlencode(params)
    try:
        response = urllib2.urlopen(hub_url, data)
    except urllib2.HTTPError, e:
        if hasattr(e, 'code') and e.code == 204:
            continue
        raise
