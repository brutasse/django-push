import datetime
import random
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

        if created:
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            secret = ''.join([random.choice(chars) for i in range(50)])
        else:
            secret = subscription.secret

        params = {
            'mode': 'subscribe',
            'callback': subscription.callback_url,
            'topic': topic,
            'verify': ('async', 'sync'),
            'verify_token': subscription.generate_token('subscribe'),
            'secret': secret,
        }
        if lease_seconds is not None:
            params['lease_seconds'] = lease_seconds
            # If not present, the lease duration is decided by the hub
        response = self.subscription_request(hub, params)

        status = response.code
        if status == 204:
            subscription.verified = True
        elif status == 202:  # deferred verification
            subscription.verified = False
        else:
            error = response.read()
            raise urllib2.HTTPError('Subscription error on %s: %s' % (topic,
                                                                      error))
        subscription.secret = secret
        subscription.save()
        return subscription

    def unsubscribe(self, topic, hub=None):
        if hub is None:
            hub = get_hub(topic)

        subscription = Subscription.objects.get(topic=topic, hub=hub)

        params = {
            'mode': 'unsubscribe',
            'callback': subscription.callback_url,
            'topic': topic,
            'verify': ('async', 'sync'),
            'verify_token': subscription.generate_token('unsubscribe'),
        }
        response = self.subscription_request(hub, params)

        if not response.code in (202, 204):
            error = response.read()
            raise urllib2.HTTPError('Unsubscription error on %s: %s' % (topic,
                                                                        error))


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
        try:
            response = urllib2.urlopen(hub, data)
            return response
        except urllib2.HTTPError, e:
            if e.code in (202, 204):
                return e
            else:
                raise


class Subscription(models.Model):
    hub = models.URLField(_('Callback'), max_length=1023)
    topic = models.URLField(_('Topic'), max_length=1023)
    verified = models.BooleanField(_('Verified'), default=False)
    verify_token = models.CharField(_('Verify Token'), max_length=255)
    lease_expiration = models.DateTimeField(_('Lease expiration'), null=True)
    secret = models.CharField(_('Secret'), max_length=255, null=True)

    objects = SubscriptionManager()

    def __unicode__(self):
        return u'%s: %s' % (self.topic, self.hub)

    def generate_token(self, mode):
        digest = sha_constructor('%s%i%s' % (settings.SECRET_KEY,
                                             self.pk, mode)).hexdigest()
        self.verify_token = mode[:20] + digest
        self.save()
        return self.verify_token

    def set_expiration(self, seconds):
        self.lease_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)
        self.save()

    def has_expired(self):
        if self.lease_expiration:
            return datetime.datetime.utcnow() > self.lease_expiration
        return False

    @property
    def callback_url(self):
        callback_url = reverse('subscriber_callback', args=[self.id])
        return 'http://%s%s' % (Site.objects.get_current(), callback_url)
