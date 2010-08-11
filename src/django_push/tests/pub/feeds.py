from django_push.publisher.feeds import Feed

from django_push.tests.pub.models import Entry


class EntryFeed(Feed):
    title = 'Latest entries'
    link = '/updates/'

    def items(self):
        return Entry.objects.filter(published=True)

    def item_title(self, item):
        return item.title

    def item_subtitle(self, item):
        return item.content

    def item_pubdate(self, item):
        return item.timestamp


class CustomHubFeed(EntryFeed):
    hub = 'http://myhub.com'
