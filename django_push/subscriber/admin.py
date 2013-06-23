from django.contrib import admin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ungettext

from django_push.subscriber.models import Subscription


class ExpirationFilter(admin.SimpleListFilter):
    title = _('Expired')
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return (
            ('true', _('Yes')),
            ('false', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(lease_expiration__lte=timezone.now())
        if self.value() == 'false':
            return queryset.filter(lease_expiration__gte=timezone.now())


class SubscriptionAmin(admin.ModelAdmin):
    list_display = ('truncated_topic', 'hub', 'verified', 'has_expired',
                    'lease_expiration')
    list_filter = ('verified', ExpirationFilter, 'hub')
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
