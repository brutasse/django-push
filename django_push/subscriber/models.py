import base64
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
from django_push.subscriber.utils import generate_random_string


class SubscriptionError(Exception):
    pass


class SubscriptionManager(models.Manager):

    def subscribe(self, topic, hub=None, **kwargs):
        if hub is None:
            hub = get_hub(topic)

        subscription, created = self.get_or_create(
            hub=hub,
            topic=topic,
            defaults={'secret': generate_random_string(),
                      }
        )

        if (not created and subscription.verified
                and not subscription.has_expired()):
            return subscription, created

        subscription.send_request(mode='subscribe', **kwargs)
        return subscription, created

    def unsubscribe(self, topic, hub=None, **kwargs):
        if hub is None:
            hub = get_hub(topic)

        try:
            subscription = Subscription.objects.get(topic=topic, hub=hub)
        except self.model.DoesNotExist:
            return

        subscription.send_request(mode='unsubscribe', **kwargs)


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

    def callback_url(self, callback_url_name):
        callback_url = reverse(callback_url_name, args=[self.id])
        use_ssl = getattr(settings, 'PUSH_SSL_CALLBACK', False)
        scheme = use_ssl and 'https' or 'http'
        return '%s://%s%s' % (scheme, Site.objects.get_current(), callback_url)

    def send_request(self, mode, **kwargs):
        callback_url = kwargs.get('callback_url_name') or 'subscriber_url'

        params = {
            'mode': mode,
            'callback': self.callback_url(callback_url),
            'topic': self.topic,
            'verify': ('async', 'sync'),
            'verify_token': self.generate_token(mode),
            'secret': self.secret,
            'lease_seconds': getattr(settings, 'PUSH_LEASE_SECONDS',
                                     60 * 60 * 24 * 30)  # defaults to 30 days
        }
        if 'extra_request_params' in kwargs:
            extra_params = kwargs['extra_request_params']
            if isinstance(extra_params, dict):
                params.update(extra_params)

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
