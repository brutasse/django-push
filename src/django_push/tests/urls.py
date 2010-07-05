from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^sub/', include('django_push.tests.sub.urls')),
    url(r'^pub/', include('django_push.tests.pub.urls')),
    url(r'^hub/', include('django_push.tests.hub.urls')),
)
