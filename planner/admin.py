from django.contrib import admin
from planner.models import UserAccount, DegreePlan, CourseGroup, CourseChoice, DegreeSchedule, Semester, Course, CourseSelection


#inlines

class CourseSelection_SemesterInline(admin.TabularInline):
	#model = CourseSelection.semester.through
	extra = 3

# class Course_CourseGroupInline(admin.TabularInline):
# 	model = Course.courseGroups.through
# 	extra = 3
# 	#exclude = ['semesters', 'courseChoices']

class CourseGroupInline(admin.TabularInline):
	model = CourseGroup
	extra = 3

class CourseChoiceInline(admin.TabularInline):
	model = CourseChoice
	extra = 3

class CourseInline(admin.TabularInline):
	model = Course.courseChoices.through
	extra = 3

class CourseSelectionInline(admin.TabularInline):
	model = CourseSelection
	extra = 3
	
#admins

class CourseGroupAdmin(admin.ModelAdmin):
	inlines = [CourseChoiceInline]

class CourseAdmin(admin.ModelAdmin):
	pass#	exclude = ('courseChoices', 'courseGroups')

class DegreePlanAdmin(admin.ModelAdmin):
	inlines = [CourseGroupInline]

class SemesterAdmin(admin.ModelAdmin):
	inlines = [CourseSelectionInline]

class UserAccountAdmin(admin.ModelAdmin):
	inlines = []

class CourseChoiceAdmin(admin.ModelAdmin):
	inlines = [CourseInline]


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(DegreePlan, DegreePlanAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
admin.site.register(CourseChoice, CourseChoiceAdmin)
admin.site.register(DegreeSchedule)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSelection)