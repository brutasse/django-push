from django.conf.urls.defaults import *
from django_push.subscriber.views import PubSubCallback

urlpatterns = patterns('',
        url(regex=r'^(?P<pk>\d+)/$', view=PubSubCallback.as_view(), name='subscriber_callback'),
)
