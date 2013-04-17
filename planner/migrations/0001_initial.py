# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserAccount'
        db.create_table(u'planner_useraccount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'planner', ['UserAccount'])

        # Adding model 'PersonalInfo'
        db.create_table(u'planner_personalinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userAccount', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.UserAccount'], unique=True)),
            ('fistName', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('lastName', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'planner', ['PersonalInfo'])

        # Adding model 'DegreePlan'
        db.create_table(u'planner_degreeplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userAccount', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.UserAccount'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'planner', ['DegreePlan'])

        # Adding model 'CourseGroup'
        db.create_table(u'planner_coursegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('degreePlan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.DegreePlan'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'planner', ['CourseGroup'])

        # Adding model 'CourseChoice'
        db.create_table(u'planner_coursechoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('courseGroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courseChoices', to=orm['planner.CourseGroup'])),
            ('courseSelected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('selectedCourse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Course'])),
        ))
        db.send_create_signal(u'planner', ['CourseChoice'])

        # Adding model 'DegreeSchedule'
        db.create_table(u'planner_degreeschedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userAccount', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['planner.UserAccount'], unique=True)),
        ))
        db.send_create_signal(u'planner', ['DegreeSchedule'])

        # Adding model 'Semester'
        db.create_table(u'planner_semester', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('degreeSched', self.gf('django.db.models.fields.related.ForeignKey')(related_name='semesters', to=orm['planner.DegreeSchedule'])),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2000)),
        ))
        db.send_create_signal(u'planner', ['Semester'])

        # Adding model 'Course'
        db.create_table(u'planner_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'planner', ['Course'])

        # Adding M2M table for field courseChoices on 'Course'
        db.create_table(u'planner_course_courseChoices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('coursechoice', models.ForeignKey(orm[u'planner.coursechoice'], null=False))
        ))
        db.create_unique(u'planner_course_courseChoices', ['course_id', 'coursechoice_id'])

        # Adding M2M table for field semesters on 'Course'
        db.create_table(u'planner_course_semesters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('semester', models.ForeignKey(orm[u'planner.semester'], null=False))
        ))
        db.create_unique(u'planner_course_semesters', ['course_id', 'semester_id'])


    def backwards(self, orm):
        # Deleting model 'UserAccount'
        db.delete_table(u'planner_useraccount')

        # Deleting model 'PersonalInfo'
        db.delete_table(u'planner_personalinfo')

        # Deleting model 'DegreePlan'
        db.delete_table(u'planner_degreeplan')

        # Deleting model 'CourseGroup'
        db.delete_table(u'planner_coursegroup')

        # Deleting model 'CourseChoice'
        db.delete_table(u'planner_coursechoice')

        # Deleting model 'DegreeSchedule'
        db.delete_table(u'planner_degreeschedule')

        # Deleting model 'Semester'
        db.delete_table(u'planner_semester')

        # Deleting model 'Course'
        db.delete_table(u'planner_course')

        # Removing M2M table for field courseChoices on 'Course'
        db.delete_table('planner_course_courseChoices')

        # Removing M2M table for field semesters on 'Course'
        db.delete_table('planner_course_semesters')


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
            'fistName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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