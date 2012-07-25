from django.contrib import admin

from django_push.subscriber.models import Subscription

admin.site.register(
    Subscription,
    list_display=['topic', 'verified', 'has_expired', 'lease_expiration'],
    search_fields=['hub', 'topic'],
)
