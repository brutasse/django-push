from django.conf.urls.defaults import *


urlpatterns = patterns('django_push.subscriber.views',
    url(r'^(?P<pk>\d+)/$', 'callback', name='subscriber_callback'),
)
