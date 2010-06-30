import datetime
import urllib
import urllib2

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

from django_push.subscriber.utils import get_hub

LEASE_SECONDS = getattr(settings, 'PUSH_LEASE_SECONDS', None)


class SubscriptionManager(models.Manager):

    def subscribe(self, topic, hub=None, lease_seconds=LEASE_SECONDS):
        if hub is None:
            hub = get_hub(topic)

        subscription, created = self.get_or_create(hub=hub, topic=topic)
        callback_url = reverse('subscriber_callback', args=[subscription.id])
        callback = 'http://%s%s' % (Site.objects.get_current(), callback_url)

        params = {
            'mode': 'subscribe',
            'callback': callback,
            'topic': topic,
            'verify': ('async', 'sync'),
            'verify_token': subscription.generate_token('subscribe'),
        }
        if lease_seconds is not None:
            params['lease_seconds'] = lease_seconds
            # If not present, the lease is permanent
        response = self.subscription_request(hub, params)

        info = response.info
        if info.status == 204:
            subscription.verified = True
        elif info.status == 202:  # deferred verification
            subscription.verified = False
        else:
            error = response.read()
            raise urllib2.HTTPError('Subscription error on %s: %s' % (topic,
                                                                      error))
        subscription.save()
        return subscription

    def subscription_request(self, hub, params):
        def get_post_data():
            for key, value in params.items():
                key = 'hub.%s' % key
                if isinstance(value, (basestring, int)):
                    yield key, str(value)
                else:
                    for subvalue in value:
                        yield key, str(subvalue)
        data = urllib.urlencode(list(get_post_data()))
        return urllib2.urlopen(hub, data)


class Subscription(models.Model):
    callback = models.URLField(_('Callback'), max_length=1023)
    topic = models.URLField(_('Topic'), max_length=1023)
    verified = models.BooleanField(_('Verified'), default=False)
    verifify_token = models.CharField(_('Verify Token'), max_length=255)
    lease_expiration = models.DateTimeField(_('Lease expiration'))

    def generate_token(self, mode):
        digest = sha_constructor('%s%i%s' % (settings.SECRET_KEY,
                                             self.pk, mode)).hexdigest()
        self.verify_token = mode[:20] + digest
        self.save()
        return self.verify_token
