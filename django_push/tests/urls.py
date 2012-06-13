from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^subscriber/', include('django_push.subscriber.urls')),
    url(r'^pub/', include('django_push.tests.pub.urls')),
)
