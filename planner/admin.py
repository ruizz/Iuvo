from django.contrib import admin
from planner.models import UserAccount
from planner.models import PersonalInfo
from planner.models import DegreePlan
from planner.models import CourseGroup
from planner.models import CourseChoice
from planner.models import DegreeSchedule
from planner.models import Semester
from planner.models import Course

admin.site.register(UserAccount)
admin.site.register(PersonalInfo)
admin.site.register(DegreePlan)
admin.site.register(CourseGroup)
admin.site.register(CourseChoice)
admin.site.register(DegreeSchedule)
admin.site.register(Semester)
admin.site.register(Course)
