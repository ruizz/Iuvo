# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseSlot'
        db.create_table(u'planner_courseslot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('isEditable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isScheduled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('courseGroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.CourseGroup'], null=True)),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Semester'], null=True)),
        ))
        db.send_create_signal(u'planner', ['CourseSlot'])

        # Adding model 'CourseGroup'
        db.create_table(u'planner_coursegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('degreePlan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.DegreePlan'], null=True)),
        ))
        db.send_create_signal(u'planner', ['CourseGroup'])

        # Adding unique constraint on 'CourseGroup', fields ['name', 'degreePlan']
        db.create_unique(u'planner_coursegroup', ['name', 'degreePlan_id'])

        # Adding unique constraint on 'Semester', fields ['userAccount', 'term', 'year']
        db.create_unique(u'planner_semester', ['userAccount_id', 'term', 'year'])

        # Adding field 'UserAccount.facebookLinked'
        db.add_column(u'planner_useraccount', 'facebookLinked',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserAccount.facebookToken'
        db.add_column(u'planner_useraccount', 'facebookToken',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


        # Changing field 'UserAccount.username'
        db.alter_column(u'planner_useraccount', 'username', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'UserAccount.school'
        db.alter_column(u'planner_useraccount', 'school', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'UserAccount.firstName'
        db.alter_column(u'planner_useraccount', 'firstName', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'UserAccount.lastName'
        db.alter_column(u'planner_useraccount', 'lastName', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'DegreePlan.name'
        db.alter_column(u'planner_degreeplan', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):
        # Removing unique constraint on 'Semester', fields ['userAccount', 'term', 'year']
        db.delete_unique(u'planner_semester', ['userAccount_id', 'term', 'year'])

        # Removing unique constraint on 'CourseGroup', fields ['name', 'degreePlan']
        db.delete_unique(u'planner_coursegroup', ['name', 'degreePlan_id'])

        # Deleting model 'CourseSlot'
        db.delete_table(u'planner_courseslot')

        # Deleting model 'CourseGroup'
        db.delete_table(u'planner_coursegroup')

        # Deleting field 'UserAccount.facebookLinked'
        db.delete_column(u'planner_useraccount', 'facebookLinked')

        # Deleting field 'UserAccount.facebookToken'
        db.delete_column(u'planner_useraccount', 'facebookToken')


        # Changing field 'UserAccount.username'
        db.alter_column(u'planner_useraccount', 'username', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'UserAccount.school'
        db.alter_column(u'planner_useraccount', 'school', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'UserAccount.firstName'
        db.alter_column(u'planner_useraccount', 'firstName', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'UserAccount.lastName'
        db.alter_column(u'planner_useraccount', 'lastName', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'DegreePlan.name'
        db.alter_column(u'planner_degreeplan', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'planner.coursegroup': {
            'Meta': {'unique_together': "(('name', 'degreePlan'),)", 'object_name': 'CourseGroup'},
            'degreePlan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.DegreePlan']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'planner.courseslot': {
            'Meta': {'object_name': 'CourseSlot'},
            'courseGroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.CourseGroup']", 'null': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isEditable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isScheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.Semester']", 'null': 'True'})
        },
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['planner.UserAccount']", 'unique': 'True', 'null': 'True'})
        },
        u'planner.semester': {
            'Meta': {'unique_together': "(('term', 'year', 'userAccount'),)", 'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.UserAccount']", 'null': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2000'})
        },
        u'planner.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'dropboxLinked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dropboxToken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'facebookLinked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebookToken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['planner']