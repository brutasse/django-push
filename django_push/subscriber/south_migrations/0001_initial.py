# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscription'
        db.create_table(u'subscriber_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hub', self.gf('django.db.models.fields.URLField')(max_length=1023)),
            ('topic', self.gf('django.db.models.fields.URLField')(max_length=1023)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('verify_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('lease_expiration', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal(u'subscriber', ['Subscription'])


    def backwards(self, orm):
        # Deleting model 'Subscription'
        db.delete_table(u'subscriber_subscription')


    models = {
        u'subscriber.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'hub': ('django.db.models.fields.URLField', [], {'max_length': '1023'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lease_expiration': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'topic': ('django.db.models.fields.URLField', [], {'max_length': '1023'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'verify_token': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['subscriber']