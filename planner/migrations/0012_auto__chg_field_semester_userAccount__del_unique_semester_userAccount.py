# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Semester', fields ['userAccount']
        db.delete_unique(u'planner_semester', ['userAccount_id'])


        # Changing field 'Semester.userAccount'
        db.alter_column(u'planner_semester', 'userAccount_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.UserAccount'], null=True))

    def backwards(self, orm):

        # Changing field 'Semester.userAccount'
        db.alter_column(u'planner_semester', 'userAccount_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.UserAccount'], unique=True, null=True))
        # Adding unique constraint on 'Semester', fields ['userAccount']
        db.create_unique(u'planner_semester', ['userAccount_id'])


    models = {
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['planner.UserAccount']", 'unique': 'True', 'null': 'True'})
        },
        u'planner.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.UserAccount']", 'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2000'})
        },
        u'planner.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'dropboxLinked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dropboxToken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['planner']