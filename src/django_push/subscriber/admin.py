from django.contrib import admin

from django_push.subscriber.models import Subscription

admin.site.register(
    Subscription,
    list_display=['topic', 'verified', 'lease_expiration'],
)
