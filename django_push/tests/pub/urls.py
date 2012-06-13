from django.conf.urls.defaults import *

from django_push.tests.pub.feeds import EntryFeed, CustomHubFeed


urlpatterns = patterns('',
    url(r'^feed/$', EntryFeed()),
    url(r'^customfeed/$', CustomHubFeed()),
)
