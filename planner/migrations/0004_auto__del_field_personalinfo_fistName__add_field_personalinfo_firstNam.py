# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PersonalInfo.fistName'
        db.delete_column(u'planner_personalinfo', 'fistName')

        # Adding field 'PersonalInfo.firstName'
        db.add_column(u'planner_personalinfo', 'firstName',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'PersonalInfo.fistName'
        raise RuntimeError("Cannot reverse this migration. 'PersonalInfo.fistName' and its values cannot be restored.")
        # Deleting field 'PersonalInfo.firstName'
        db.delete_column(u'planner_personalinfo', 'firstName')


    models = {
        u'planner.course': {
            'Meta': {'object_name': 'Course'},
            'courseChoices': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'courses'", 'symmetrical': 'False', 'to': u"orm['planner.CourseChoice']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'semesters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'courses'", 'symmetrical': 'False', 'to': u"orm['planner.Semester']"})
        },
        u'planner.coursechoice': {
            'Meta': {'object_name': 'CourseChoice'},
            'courseGroup': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courseChoices'", 'to': u"orm['planner.CourseGroup']"}),
            'courseSelected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'selectedCourse': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.Course']"})
        },
        u'planner.coursegroup': {
            'Meta': {'object_name': 'CourseGroup'},
            'degreePlan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.DegreePlan']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['planner.UserAccount']", 'unique': 'True'})
        },
        u'planner.degreeschedule': {
            'Meta': {'object_name': 'DegreeSchedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['planner.UserAccount']", 'unique': 'True'})
        },
        u'planner.personalinfo': {
            'Meta': {'object_name': 'PersonalInfo'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['planner.UserAccount']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'planner.semester': {
            'Meta': {'object_name': 'Semester'},
            'degreeSched': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'semesters'", 'to': u"orm['planner.DegreeSchedule']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2000'})
        },
        u'planner.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['planner']