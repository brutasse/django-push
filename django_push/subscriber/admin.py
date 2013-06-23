from django.contrib import admin

from django_push.subscriber.models import Subscription


class SubscriptionAmin(admin.ModelAdmin):
    list_display = ('truncated_topic', 'hub', 'verified', 'lease_expiration')
    list_filter = ('verified', 'hub')
    search_fields = ('topic', 'hub')

admin.site.register(Subscription, SubscriptionAmin)
