from django.conf.urls import patterns, url, include


urlpatterns = patterns(
    '',
    url(r'^subscriber/', include('django_push.subscriber.urls')),
)
