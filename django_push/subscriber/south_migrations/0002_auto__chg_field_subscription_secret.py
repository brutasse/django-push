# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Subscription.secret'
        db.alter_column(u'subscriber_subscription', 'secret', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

    def backwards(self, orm):

        # Changing field 'Subscription.secret'
        db.alter_column(u'subscriber_subscription', 'secret', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    models = {
        u'subscriber.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'hub': ('django.db.models.fields.URLField', [], {'max_length': '1023'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lease_expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'topic': ('django.db.models.fields.URLField', [], {'max_length': '1023'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verify_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['subscriber']