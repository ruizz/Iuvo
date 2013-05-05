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
	list_display = ('name', 'degreePlan', 'colNum')

class CourseAdmin(admin.ModelAdmin):
	extra = 3

class DegreePlanAdmin(admin.ModelAdmin):
	inlines = [CourseGroupInline]
	list_display = ('name', 'major')

class SemesterAdmin(admin.ModelAdmin):
	inlines = [CourseSelectionInline]
	list_display = ('term', 'year', 'degreeSched')

class UserAccountAdmin(admin.ModelAdmin):
	inlines = []
	list_display = ('firstName', 'lastName', 'username', 'school', 'degreePlan', 'dropboxLinked', 'dropboxToken')

class CourseChoiceAdmin(admin.ModelAdmin):
	inlines = [CourseInline]
	list_display = ('name', 'courseGroup', 'required')

admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(DegreePlan, DegreePlanAdmin)
admin.site.register(CourseGroup, CourseGroupAdmin)
admin.site.register(CourseChoice, CourseChoiceAdmin)
admin.site.register(DegreeSchedule)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSelection)