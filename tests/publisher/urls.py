from django.conf.urls import url, patterns

from .feeds import HubFeed, OverrideHubFeed, DynamicHubFeed


urlpatterns = patterns(
    '',
    url(r'^feed/$', HubFeed(), name='feed'),
    url(r'^override-feed/$', OverrideHubFeed(), name='override-feed'),
    url(r'^dynamic-feed/$', DynamicHubFeed(), name='dynamic-feed'),
)
