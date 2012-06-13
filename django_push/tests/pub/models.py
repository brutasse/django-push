import datetime

from django.db import models

from django_push.publisher import ping_hub


class Entry(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        return '/some-url'

    class Meta:
        ordering = ('-timestamp',)

    def publish(self):
        self.published = True
        self.timestamp = datetime.datetime.utcnow()
        self.save()

        ping_hub('http://testserver/pub/feed/')  # Don't hardocde like that
