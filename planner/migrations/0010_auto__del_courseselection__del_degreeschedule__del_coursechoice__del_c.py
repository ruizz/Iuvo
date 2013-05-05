# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CourseSelection'
        db.delete_table(u'planner_courseselection')

        # Deleting model 'DegreeSchedule'
        db.delete_table(u'planner_degreeschedule')

        # Deleting model 'CourseChoice'
        db.delete_table(u'planner_coursechoice')

        # Deleting model 'CourseGroup'
        db.delete_table(u'planner_coursegroup')

        # Deleting model 'Course'
        db.delete_table(u'planner_course')

        # Removing M2M table for field courseChoices on 'Course'
        db.delete_table('planner_course_courseChoices')

        # Deleting field 'Semester.degreeSched'
        db.delete_column(u'planner_semester', 'degreeSched_id')

        # Deleting field 'UserAccount.degreePlan'
        db.delete_column(u'planner_useraccount', 'degreePlan_id')

        # Deleting field 'DegreePlan.major'
        db.delete_column(u'planner_degreeplan', 'major')

        # Adding field 'DegreePlan.userAccount'
        db.add_column(u'planner_degreeplan', 'userAccount',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.UserAccount'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'CourseSelection'
        db.create_table(u'planner_courseselection', (
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='selections', null=True, to=orm['planner.Semester'], blank=True)),
            ('selectedCourse', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='selections', null=True, to=orm['planner.Course'], blank=True)),
            ('userAccount', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['planner.UserAccount'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('courseChoice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['planner.CourseChoice'])),
        ))
        db.send_create_signal(u'planner', ['CourseSelection'])

        # Adding model 'DegreeSchedule'
        db.create_table(u'planner_degreeschedule', (
            ('userAccount', self.gf('django.db.models.fields.related.OneToOneField')(related_name='degreeSchedule', unique=True, to=orm['planner.UserAccount'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'planner', ['DegreeSchedule'])

        # Adding model 'CourseChoice'
        db.create_table(u'planner_coursechoice', (
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('courseGroup', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courseChoices', to=orm['planner.CourseGroup'])),
        ))
        db.send_create_signal(u'planner', ['CourseChoice'])

        # Adding model 'CourseGroup'
        db.create_table(u'planner_coursegroup', (
            ('colNum', self.gf('django.db.models.fields.IntegerField')(default=1)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('degreePlan', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courseGroups', to=orm['planner.DegreePlan'])),
        ))
        db.send_create_signal(u'planner', ['CourseGroup'])

        # Adding model 'Course'
        db.create_table(u'planner_course', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hours', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=4)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'planner', ['Course'])

        # Adding M2M table for field courseChoices on 'Course'
        db.create_table(u'planner_course_courseChoices', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'planner.course'], null=False)),
            ('coursechoice', models.ForeignKey(orm[u'planner.coursechoice'], null=False))
        ))
        db.create_unique(u'planner_course_courseChoices', ['course_id', 'coursechoice_id'])


        # User chose to not deal with backwards NULL issues for 'Semester.degreeSched'
        raise RuntimeError("Cannot reverse this migration. 'Semester.degreeSched' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'UserAccount.degreePlan'
        raise RuntimeError("Cannot reverse this migration. 'UserAccount.degreePlan' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'DegreePlan.major'
        raise RuntimeError("Cannot reverse this migration. 'DegreePlan.major' and its values cannot be restored.")
        # Deleting field 'DegreePlan.userAccount'
        db.delete_column(u'planner_degreeplan', 'userAccount_id')


    models = {
        u'planner.degreeplan': {
            'Meta': {'object_name': 'DegreePlan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'userAccount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['planner.UserAccount']", 'null': 'True'})
        },
        u'planner.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
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