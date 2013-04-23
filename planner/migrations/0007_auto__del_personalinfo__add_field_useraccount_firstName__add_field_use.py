# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PersonalInfo'
        db.delete_table(u'planner_personalinfo')

        # Adding field 'UserAccount.firstName'
        db.add_column(u'planner_useraccount', 'firstName',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'UserAccount.lastName'
        db.add_column(u'planner_useraccount', 'lastName',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'UserAccount.username'
        db.add_column(u'planner_useraccount', 'username',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'UserAccount.school'
        db.add_column(u'planner_useraccount', 'school',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'PersonalInfo'
        db.create_table(u'planner_personalinfo', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('firstName', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('userAccount', self.gf('django.db.models.fields.related.OneToOneField')(related_name='personlInfo', unique=True, to=orm['planner.UserAccount'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'planner', ['PersonalInfo'])

        # Deleting field 'UserAccount.firstName'
        db.delete_column(u'planner_useraccount', 'firstName')

        # Deleting field 'UserAccount.lastName'
        db.delete_column(u'planner_useraccount', 'lastName')

        # Deleting field 'UserAccount.username'
        db.delete_column(u'planner_useraccount', 'username')

        # Deleting field 'UserAccount.school'
        db.delete_column(u'planner_useraccount', 'school')


    models = {
        u'planner.course': {
            'Meta': {'object_name': 'Course'},
            'courseChoices': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'courses'", 'blank': 'True', 'to': u"orm['planner.CourseChoice']"}),
            'courseGroups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'courses'", 'blank': 'True', 'to': u"orm['planner.CourseGroup']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'hours': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'semesters': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'courses'", 'blank': 'True', 'to': u"orm['planner.Semester']"})
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
        u'planner.semester': {
            'Meta': {'object_name': 'Semester'},
            'degreeSched': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'semesters'", 'to': u"orm['planner.DegreeSchedule']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2000'})
        },
        u'planner.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'firstName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['planner']