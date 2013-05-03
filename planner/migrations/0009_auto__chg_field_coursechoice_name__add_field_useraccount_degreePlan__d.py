# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CourseChoice.name'
        db.alter_column(u'planner_coursechoice', 'name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))
        # Adding field 'UserAccount.degreePlan'
        db.add_column(u'planner_useraccount', 'degreePlan',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['planner.DegreePlan']),
                      keep_default=False)

        # Deleting field 'DegreePlan.userAccount'
        db.delete_column(u'planner_degreeplan', 'userAccount_id')


    def backwards(self, orm):

        # Changing field 'CourseChoice.name'
        db.alter_column(u'planner_coursechoice', 'name', self.gf('django.db.models.fields.CharField')(default='NULL', max_length=200))
        # Deleting field 'UserAccount.degreePlan'
        db.delete_column(u'planner_useraccount', 'degreePlan_id')

        # Adding field 'DegreePlan.userAccount'
        db.add_column(u'planner_degreeplan', 'userAccount',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='degreePlan', unique=True, to=orm['planner.UserAccount']),
                      keep_default=False)


    models = {
        u'planner.course': {
            'Meta': {'object_name': 'Course'},
            'courseChoices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'courses'", 'blank': 'True', 'to': u"orm['planner.CourseChoice']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'planner.coursechoice': {
            'Meta': {'object_name': 'CourseChoice'},
            'courseGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courseChoices'", 'to': u"orm['planner.CourseGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'planner.coursegroup': {
            'Meta': {'object_name': 'CourseGroup'},
            'colNum': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'degreePlan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courseGroups'", 'to': u"orm['planner.DegreePlan']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'planner.courseselection': {
            'Meta': {'object_name': 'CourseSelection'},
            'courseChoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': u"orm['planner.CourseChoice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'selectedCourse': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'selections'", 'null': 'True', 'blank': 'True', 'to': u"orm['planner.Course']"}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'selections'", 'null': 'True', 'blank': 'True', 'to': u"orm['planner.Semester']"}),
            'userAccount': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': u"orm['planner.UserAccount']"})
        },
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'planner.degreeschedule': {
            'Meta': {'object_name': 'DegreeSchedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'degreeSchedule'", 'unique': 'True', 'to': u"orm['planner.UserAccount']"})
        },
        u'planner.semester': {
            'Meta': {'object_name': 'Semester'},
            'degreeSched': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'semesters'", 'to': u"orm['planner.DegreeSchedule']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2000'})
        },
        u'planner.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'degreePlan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.DegreePlan']"}),
            'dropboxLinked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dropboxToken': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['planner']