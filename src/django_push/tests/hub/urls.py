from django.conf.urls.defaults import *


urlpatterns = patterns('hub.views',
    url(r'^$', 'ping', name='ping'),
)
