import feedparser
import hashlib
import hmac

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django_push.subscriber.models import Subscription, SubscriptionError
from django_push.subscriber.signals import updated


@csrf_exempt
def callback(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk)

    if request.method == 'GET':
        mode = request.GET['hub.mode']
        topic = request.GET['hub.topic']
        challenge = request.GET['hub.challenge']
        lease_seconds = request.GET.get('hub.lease_seconds', None)
        verify_token = request.GET.get('hub.verify_token', None)

        if mode == 'subscribe':
            if not verify_token.startswith(mode):
                raise Http404

            invalid_subscription = any((
                all((
                    verify_token is not None,
                    subscription.verify_token != verify_token,
                )),
                topic != subscription.topic,
            ))
            if invalid_subscription:
                raise Http404

            subscription.verified = True
            if lease_seconds is not None:
                subscription.set_expiration(int(lease_seconds))

            subscription.save()
            return HttpResponse(challenge)

        if mode == 'unsubscribe':
            subscription.delete()
            return HttpResponse(challenge)

    elif request.method == 'POST':
        signature = request.META.get('HTTP_X_HUB_SIGNATURE', None)
        if subscription.secret:
            if signature is None:
                # Acknowledging receipt but ignoring the message
                return HttpResponse('')

            hasher = hmac.new(str(subscription.secret),
                              request.raw_post_data,
                              hashlib.sha1)
            digest = 'sha1=%s' % hasher.hexdigest()
            if signature != digest:
                return HttpResponse('')

        parsed = feedparser.parse(request.raw_post_data)
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
                try:
                    Subscription.objects.subscribe(topic_url, hub=hub_url)
                except SubscriptionError:
                    pass

            updated.send(sender=subscription, notification=parsed)
            return HttpResponse('')

        return HttpResponse()
