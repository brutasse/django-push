from django.conf.urls import patterns, url

from .views import callback


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', callback, name='subscriber_callback'),
)
