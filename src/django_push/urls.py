from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^sub/', include('django_push.subscriber.urls')),
)
