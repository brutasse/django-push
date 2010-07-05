from django.conf import settings
from django.contrib.syndication.views import Feed as BaseFeed
from django.utils.feedgenerator import Atom1Feed


class HubAtom1Feed(Atom1Feed):
    def add_root_elements(self, handler):
        super(HubAtom1Feed, self).add_root_elements(handler)

        hub = self.feed.get('hub')
        if hub is not None:
            handler.addQuickElement(u'link', '', {u'rel': u'hub',
                                                  u'href': hub})


class Feed(BaseFeed):
    feed_type = HubAtom1Feed
    hub = getattr(settings, 'PUSH_HUB')

    def feed_extra_kwargs(self, obj):
        return {'hub': self.hub}
