import base64
import random
import urllib
import urllib2

from datetime import timedelta
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

from django_push.subscriber.utils import get_hub, get_hub_credentials


class SubscriptionError(Exception):
    pass


class SubscriptionManager(models.Manager):
    """
    'create_subscription' method only creates an intance of Subscription but
    does not send the request to the server. To initialte request you have to
    make sure that the instance has been commited to the database before you
    do that. In a Django view, that means you have to call transaction commit
    manually before calling subscription.send_request('subscribe')
    """

    def get_or_create_subscription(self, topic, hub=None):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

        if hub is None:
            hub = get_hub(topic)

        subscription, created = self.get_or_create(hub=hub,
                                                   topic=topic,
                                                   defaults={'secret': ''.join([random.choice(chars) for i in range(50)]),
                                                             })
        return subscription

    def unsubscribe(self, topic, hub=None):
        if hub is None:
            hub = get_hub(topic)

        subscription = Subscription.objects.get(topic=topic, hub=hub)

        subscription.send_request(mode='unsubscribe')


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
        self.lease_expiration = timezone.now() + timedelta(seconds=seconds)
        self.save()

    def has_expired(self):
        if self.lease_expiration:
            return timezone.now() > self.lease_expiration
        return False

    @property
    def callback_url(self):
        callback_url = reverse('subscriber_callback', args=[self.id])
        use_ssl = getattr(settings, 'PUSH_SSL_CALLBACK', False)
        scheme = use_ssl and 'https' or 'http'
        return '%s://%s%s' % (scheme, Site.objects.get_current(), callback_url)

    def send_request(self, mode):
        if self.verified and not self.has_expired():
            return

        params = {
            'mode': mode,
            'callback': self.callback_url,
            'topic': self.topic,
            'verify': ('async', 'sync'),
            'verify_token': self.generate_token(mode),
            'secret': self.secret,
            'lease_seconds': getattr(settings, 'PUSH_LEASE_SECONDS')
        }

        def _get_post_data():
            for key, value in params.items():
                key = 'hub.%s' % key
                if isinstance(value, (basestring, int)):
                    yield key, str(value)
                else:
                    for subvalue in value:
                        yield key, str(subvalue)

        data = urllib.urlencode(list(_get_post_data()))

        try:
            headers = {}
            credentials = get_hub_credentials(self.hub)
            if credentials is not None:
                username, password = credentials
                encoded = base64.encodestring(
                    "%s:%s" % (username, password))[:-1]
                headers['Authorization'] = "Basic %s" % encoded
            request = urllib2.Request(self.hub, data, headers)
            response = urllib2.urlopen(request)

        except urllib2.HTTPError, e:
            if e.code in (202, 204):
                return e
            #else
            # FIXME re-raising may throw a 500 error on notifications
            #    raise
            return e

        status = response.code
        if status in (202, 204):  # 202: deferred verification
            self.verified = True
        else:
            error = response.read()
            raise SubscriptionError('Subscription error on %s: %s' % (self.topic,
                                                                      error))
        self.save()
