import feedparser


def get_hub(topic):
    parsed = feedparser.parse(topic)
    for link in parsed.feed.links:
        if link['rel'] == 'hub':
            return link['href']
    raise TypeError, "Hub not found"
