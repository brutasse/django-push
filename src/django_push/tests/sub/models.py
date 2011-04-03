from django_push.subscriber.signals import updated


def listener(notification, **kwargs):
    for entry in notification.entries:
        if 'title' in entry:
            print entry.title

updated.connect(listener)
