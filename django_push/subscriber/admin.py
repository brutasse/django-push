from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, ungettext

from django_push.subscriber.models import Subscription


class SubscriptionAmin(admin.ModelAdmin):
    list_display = ('truncated_topic', 'hub', 'verified', 'has_expired',
                    'lease_expiration')
    list_filter = ('verified', 'hub')
    search_fields = ('topic', 'hub')
    actions = ['renew', 'unsubscribe']

    def renew(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.subscribe()
            count += 1
        message = ungettext(
            '%s subscription was successfully renewed.',
            '%s subscriptions were successfully renewd.',
            count) % count
        self.message_user(request, message)
    renew.short_description = _('Renew selected subscriptions')

    def unsubscribe(self, request, queryset):
        count = 0
        for subscription in queryset:
            subscription.unsubscribe()
            count += 1
        message = ungettext(
            'Successfully unsubscribed from %s topic.',
            'Successfully unsubscribed from %s topics.',
            count) % count
        self.message_user(request, message)
    unsubscribe.short_description = _('Unsubscribe from selected topics')
admin.site.register(Subscription, SubscriptionAmin)
