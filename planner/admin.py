from django.contrib import admin
from planner.models import UserAccount, DegreePlan, CourseGroup, CourseChoice, DegreeSchedule, Semester, Course


#inlines

class Course_SemesterInline(admin.TabularInline):
	model = Course.semesters.through
	extra = 3

class Course_CourseGroupInline(admin.TabularInline):
	model = Course.courseGroups.through
	extra = 3
	#exclude = ['semesters', 'courseChoices']

class CourseGroupInline(admin.TabularInline):
	model = CourseGroup
	extra = 3


#admins

class CourseGroupAdmin(admin.ModelAdmin):
	inlines = [Course_CourseGroupInline]

class CourseAdmin(admin.ModelAdmin):
	pass#	exclude = ('courseChoices', 'courseGroups')

class DegreePlanAdmin(admin.ModelAdmin):
	inlines = [CourseGroupInline]

class SemesterAdmin(admin.ModelAdmin):
	inlines = [Course_SemesterInline]

class UserAccountAdmin(admin.ModelAdmin):
	inlines = []


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(DegreePlan, DegreePlanAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
admin.site.register(CourseChoice)
admin.site.register(DegreeSchedule)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
