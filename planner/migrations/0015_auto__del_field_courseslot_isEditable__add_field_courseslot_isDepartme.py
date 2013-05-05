# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CourseSlot.isEditable'
        db.delete_column(u'planner_courseslot', 'isEditable')

        # Adding field 'CourseSlot.isDepartmentEditable'
        db.add_column(u'planner_courseslot', 'isDepartmentEditable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CourseSlot.isNumberEditable'
        db.add_column(u'planner_courseslot', 'isNumberEditable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'CourseSlot.notes'
        db.alter_column(u'planner_courseslot', 'notes', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True))

    def backwards(self, orm):
        # Adding field 'CourseSlot.isEditable'
        db.add_column(u'planner_courseslot', 'isEditable',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'CourseSlot.isDepartmentEditable'
        db.delete_column(u'planner_courseslot', 'isDepartmentEditable')

        # Deleting field 'CourseSlot.isNumberEditable'
        db.delete_column(u'planner_courseslot', 'isNumberEditable')


        # Changing field 'CourseSlot.notes'
        db.alter_column(u'planner_courseslot', 'notes', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        u'planner.coursegroup': {
            'Meta': {'unique_together': "(('name', 'degreePlan'),)", 'object_name': 'CourseGroup'},
            'degreePlan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.DegreePlan']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'planner.courseslot': {
            'Meta': {'object_name': 'CourseSlot'},
            'courseGroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.CourseGroup']", 'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isDepartmentEditable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isNumberEditable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isScheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.Semester']", 'null': 'True', 'blank': 'True'})
        },
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['planner.UserAccount']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'planner.semester': {
            'Meta': {'unique_together': "(('term', 'year', 'userAccount'),)", 'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'userAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.UserAccount']", 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '20'})
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