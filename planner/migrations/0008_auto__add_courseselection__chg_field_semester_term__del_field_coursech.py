# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseSelection'
        db.create_table(u'planner_courseselection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('selectedCourse', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='selections', null=True, blank=True, to=orm['planner.Course'])),
            ('userAccount', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['planner.UserAccount'])),
            ('courseChoice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['planner.CourseChoice'])),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='selections', null=True, blank=True, to=orm['planner.Semester'])),
        ))
        db.send_create_signal(u'planner', ['CourseSelection'])


        # Changing field 'Semester.term'
        db.alter_column(u'planner_semester', 'term', self.gf('django.db.models.fields.CharField')(max_length=2))
        # Deleting field 'CourseChoice.selectedCourse'
        db.delete_column(u'planner_coursechoice', 'selectedCourse_id')

        # Deleting field 'CourseChoice.courseSelected'
        db.delete_column(u'planner_coursechoice', 'courseSelected')

        # Adding field 'CourseChoice.required'
        db.add_column(u'planner_coursechoice', 'required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CourseGroup.colNum'
        db.add_column(u'planner_coursegroup', 'colNum',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Removing M2M table for field semesters on 'Course'
        db.delete_table('planner_course_semesters')

        # Removing M2M table for field courseGroups on 'Course'
        db.delete_table('planner_course_courseGroups')

        # Adding field 'UserAccount.dropboxLinked'
        db.add_column(u'planner_useraccount', 'dropboxLinked',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserAccount.dropboxToken'
        db.add_column(u'planner_useraccount', 'dropboxToken',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'CourseSelection'
        db.delete_table(u'planner_courseselection')


        # Changing field 'Semester.term'
        db.alter_column(u'planner_semester', 'term', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Adding field 'CourseChoice.selectedCourse'
        db.add_column(u'planner_coursechoice', 'selectedCourse',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['planner.Course']),
                      keep_default=False)

        # Adding field 'CourseChoice.courseSelected'
        db.add_column(u'planner_coursechoice', 'courseSelected',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'CourseChoice.required'
        db.delete_column(u'planner_coursechoice', 'required')

        # Deleting field 'CourseGroup.colNum'
        db.delete_column(u'planner_coursegroup', 'colNum')

        # Adding M2M table for field semesters on 'Course'
        db.create_table(u'planner_course_semesters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('semester', models.ForeignKey(orm[u'planner.semester'], null=False))
        ))
        db.create_unique(u'planner_course_semesters', ['course_id', 'semester_id'])

        # Adding M2M table for field courseGroups on 'Course'
        db.create_table(u'planner_course_courseGroups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('coursegroup', models.ForeignKey(orm[u'planner.coursegroup'], null=False))
        ))
        db.create_unique(u'planner_course_courseGroups', ['course_id', 'coursegroup_id'])

        # Deleting field 'UserAccount.dropboxLinked'
        db.delete_column(u'planner_useraccount', 'dropboxLinked')

        # Deleting field 'UserAccount.dropboxToken'
        db.delete_column(u'planner_useraccount', 'dropboxToken')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2000'})
        },
        u'planner.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
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