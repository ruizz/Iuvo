from django.contrib import admin
from planner.models import *

class DegreePlanInline(admin.TabularInline):
	model = DegreePlan
	extra = 0

class SemesterInline(admin.TabularInline):
	model = Semester
	extra = 10

class CourseGroupInline(admin.TabularInline):
	model = CourseGroup
	extra = 10
	
class CourseSlotInline(admin.TabularInline):
	model = CourseSlot
	extra = 20

class UserAccountAdmin(admin.ModelAdmin):
	inlines = [DegreePlanInline, SemesterInline]
	list_display = ('firstName', 'lastName', 'username', 'school', 'dropboxLinked', 'facebookLinked', 'dropboxToken', 'facebookToken', )

class DegreePlanAdmin(admin.ModelAdmin):
	inlines = [CourseGroupInline]
	list_display = ('name', 'userAccount',)
	
class SemesterAdmin(admin.ModelAdmin):
	inlines = [CourseSlotInline]
	list_display = ('term', 'year', 'userAccount',)
	
class CourseGroupAdmin(admin.ModelAdmin):
	inlines = [CourseSlotInline]
	list_display = ('name', 'degreePlan', )
	
class CourseSlotAdmin(admin.ModelAdmin):
	list_display = ('department', 'number', 'hours', 'isDepartmentEditable', 'isNumberEditable', 'isScheduled', 'notes', 'courseGroup', 'semester', )
	
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(DegreePlan, DegreePlanAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
admin.site.register(CourseSlot, CourseSlotAdmin)