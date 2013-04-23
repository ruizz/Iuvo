# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field semesters on 'Course'
        db.delete_table('planner_course_semesters')

        # Adding M2M table for field courseGroups on 'Course'
        db.create_table(u'planner_course_courseGroups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('coursegroup', models.ForeignKey(orm[u'planner.coursegroup'], null=False))
        ))
        db.create_unique(u'planner_course_courseGroups', ['course_id', 'coursegroup_id'])


    def backwards(self, orm):
        # Adding M2M table for field semesters on 'Course'
        db.create_table(u'planner_course_semesters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('semester', models.ForeignKey(orm[u'planner.semester'], null=False))
        ))
        db.create_unique(u'planner_course_semesters', ['course_id', 'semester_id'])

        # Removing M2M table for field courseGroups on 'Course'
        db.delete_table('planner_course_courseGroups')


    models = {
        u'planner.course': {
            'Meta': {'object_name': 'Course'},
            'courseChoices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'courses'", 'blank': 'True', 'to': u"orm['planner.CourseChoice']"}),
            'courseGroups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'courses'", 'symmetrical': 'False', 'to': u"orm['planner.CourseGroup']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'degreePlan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courseGroups'", 'to': u"orm['planner.DegreePlan']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'degreePlan'", 'unique': 'True', 'to': u"orm['planner.UserAccount']"})
        },
        u'planner.degreeschedule': {
            'Meta': {'object_name': 'DegreeSchedule'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'degreeSchedule'", 'unique': 'True', 'to': u"orm['planner.UserAccount']"})
        },
        u'planner.personalinfo': {
            'Meta': {'object_name': 'PersonalInfo'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userAccount': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'personlInfo'", 'unique': 'True', 'to': u"orm['planner.UserAccount']"}),
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