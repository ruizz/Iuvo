from django.contrib import admin
from planner.models import UserAccount, PersonalInfo, DegreePlan, CourseGroup, CourseChoice, DegreeSchedule, Semester, Course

admin.site.register(UserAccount)
admin.site.register(PersonalInfo)
admin.site.register(DegreePlan)
admin.site.register(CourseGroup)
admin.site.register(CourseChoice)
admin.site.register(DegreeSchedule)
admin.site.register(Semester)
admin.site.register(Course)
