from django.db import models

# One for every user, auto-generated whenever a user signs up for Facebook the first time.
class UserAccount(models.Model):
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	username = models.CharField(max_length=20)
	school = models.CharField(max_length=50)
	dropboxLinked = models.BooleanField(default=False)
	dropboxToken = models.CharField(max_length=100, default="", blank=True)
	dropboxTokenSecret = models.CharField(max_length=100, default="", blank=True)
	facebookLinked = models.BooleanField(default=False)
	facebookToken = models.CharField(max_length=1000, default="", blank=True)
	def semesterOrder(self):
		return self.semester_set.all().order_by('year')
	def __unicode__(self):
		return self.lastName + ", " + self.firstName

# Degree Plan, comes free with a user account.
# A Computer Science degree plan is created using a function in degrees.py.
class DegreePlan(models.Model):
	name = models.CharField(max_length=50)
	userAccount = models.ForeignKey(UserAccount, null=True, blank=True, unique=True)
	def __unicode__(self):
		return self.name + " (" + self.userAccount.username + ")"

# Semester, created by the user. Each one is linked to a user account via ForeignKey, same as DegreePlan.
class Semester(models.Model):
	TERMS = (('CC', 'Fall'), ('AA', 'Spring'), ('BB', 'Summer'), )
	term = models.CharField(max_length=2, choices=TERMS)
	year = models.IntegerField(default=20)
	userAccount = models.ForeignKey(UserAccount, null=True, blank=True)
	
	# Prevent duplicate semesters created by the user.
	class Meta:
		unique_together = ("term", "year", "userAccount",)
	
	# Returns a formal name for the term, since our terms are essentially codes.
	def termFullName(self):
		if self.term == "CC":
			return "FALL"
		elif self.term == "AA":
			return "SPRING"
		else:
			return "SUMMER"
	
	# Returns nice, english string for when users tweet about the classes that they're
	# 	taking for that semester.
	def twitterString(self):
		string = "I'm taking "
		css = self.courseslot_set.all()
		if css:
			if len(css) > 2:
				for cs in css:
					if not cs == css[len(css)-1]:
						string += cs.department + " " + str(cs.number) + ", "
					else:
						string += "and " + cs.department + " " + str(cs.number) + " "
			elif len(css) == 2:
				for cs in css:
					if not cs == css[len(css)-1]:
						string += cs.department + " " + str(cs.number) + " "
					else:
						string += "and " + cs.department + " " + str(cs.number) + " "
			else:
				string += css[0].department + " " + str(css[0].number) + " "
		else:
			string += "nothing "
		
		if self.term == "AA":
			string += "for Spring "
		elif self.term == "BB":
			string += "for Summer "
		else:
			string += "for Fall "
		string += str(self.year) + "."
		return string
	
	# Self definition for querying.
	def __unicode__(self):
		return self.term + " " + str(self.year) + " (" + self.userAccount.username + ")"

# Ex: International & Cultural Diversity
class CourseGroup(models.Model):
	name = models.CharField(max_length=50)
	
	# Degree plan that this group is tied to.
	degreePlan = models.ForeignKey(DegreePlan, null=True, blank=True)
	
	# Degree plans are displayed in three columns. Course groups go in one of three of them
	# Options are 0, 1, or 2.
	columnNumber = models.IntegerField(default=0)
	
	# Though user doesn't create course groups (yet), this prevents an admin from creating
	#	two of the exact same course group.
	class Meta:
		unique_together = ("name", "degreePlan",)
		
	# Self definition for querying.
	def __unicode__(self):
		return self.name

# Individual Courses, EX: MATH 151
class CourseSlot(models.Model):
	department = models.CharField(max_length=4, blank=True) # Ex: CSCE
	number = models.IntegerField(default=0, blank=True) # EX: 151
	hours = models.IntegerField(default=3) # EX: 3
	isCompleted = models.BooleanField(default=False) # User specifies if course has been completed.
	isDepartmentEditable = models.BooleanField(default=False) # If user can change the department name
	isNumberEditable = models.BooleanField(default=False) # If user can change the department number
	isScheduled = models.BooleanField(default=False) # Has the user assigned this course to a semester yet?
	notes = models.CharField(max_length=1000, null=True, blank=True) # Any additional notes about the class
	courseGroup = models.ForeignKey(CourseGroup, null=True, blank=True) # Course group that this course belongs to.
	semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.SET_NULL)	# User specifies which semester this course is being taken.
	
	# Self definition for querying.
	def __unicode__(self):
		return self.department + " " + str(self.number) + " (" + str(self.hours) + ")"
		
# python manage.py schemamigration planner --auto
# python manage.py migrate planner
