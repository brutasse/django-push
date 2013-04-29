import feedparser
import hashlib
import hmac

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from django_push.subscriber.models import Subscription


class PubSubCallback(View):
    MODE_SUBSCRIBE = 'subscribe'
    MODE_UNSUBSCRIBE = 'unsubscribe'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PubSubCallback, self).dispatch(*args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        try:
            subscription = Subscription.objects.get(pk=pk)
            mode = request.GET['hub.mode']
            topic = request.GET['hub.topic']
            challenge = request.GET['hub.challenge']
            verify_token = request.GET['hub.verify_token']
            lease_seconds = request.GET.get('hub.lease_seconds', None)
        except (Subscription.DoesNotExist, KeyError):
            raise Http404

        valid_request = all((
            verify_token.startswith(mode),
            verify_token == subscription.verify_token,
            topic == subscription.topic
        ))

        if valid_request:
            if mode == self.MODE_SUBSCRIBE:
                subscription.verified = True
                if lease_seconds is not None:
                    subscription.set_expiration(int(lease_seconds))
                subscription.save()

            if mode == self.MODE_UNSUBSCRIBE:
                subscription.delete()

            return HttpResponse(challenge)

        raise Http404

    def post(self, request, pk, *args, **kwargs):
        subscription = get_object_or_404(Subscription, pk=pk)
        signature = request.META.get('HTTP_X_HUB_SIGNATURE', None)
        if subscription.secret and signature is not None:
            hasher = hmac.new(str(subscription.secret),
                              request.raw_post_data,
                              hashlib.sha1)
            digest = 'sha1=%s' % hasher.hexdigest()
            if signature != digest:
                return HttpResponse(status=400)

        parsed = feedparser.parse(request.body)
        links = getattr(parsed.feed, 'links', None)
        if links:
            hub_url = subscription.hub
            topic_url = subscription.topic
            for link in links:
                if link['rel'] == 'hub':
                    hub_url = link['href']
                elif link['rel'] == 'self':
                    topic_url = link['href']

            needs_update = any((
                hub_url and subscription.hub != hub_url,
                topic_url != subscription.topic,
            ))

            if needs_update:
                return self.subscription_updated(subscription, parsed)

            return self.feed_update(subscription, parsed)

        return HttpResponse()

    def feed_update(self, subscription, feed):
        """
        Override this in the subclass view to handle the updated feed.
        """
        return HttpResponse(status=200)

    def subscription_updated(self, subscription, feed):
        """
        Override this in the subclass view to handle the changed subscription.
        """
        return HttpResponse(status=200)
