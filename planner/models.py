from django.db import models

class UserAccount(models.Model):
	firstName = models.CharField(max_length=50)
	lastName = models.CharField(max_length=50)
	username = models.CharField(max_length=20)
	school = models.CharField(max_length=50)
	dropboxLinked = models.BooleanField(default=False)
	dropboxToken = models.CharField(max_length=50, default="", blank=True)
	facebookLinked = models.BooleanField(default=False)
	facebookToken = models.CharField(max_length=1000, default="", blank=True)
	def semesterOrder(self):
		return self.semester_set.all().order_by('year')
	def __unicode__(self):
		return self.lastName + ", " + self.firstName
	
class DegreePlan(models.Model):
	name = models.CharField(max_length=50)
	userAccount = models.ForeignKey(UserAccount, null=True, blank=True, unique=True)
	def __unicode__(self):
		return self.name + " (" + self.userAccount.username + ")"

class Semester(models.Model):
	TERMS = (
		('CC', 'Fall'),
		('AA', 'Spring'),
		('BB', 'Summer'),
		)
	term = models.CharField(max_length=2, choices=TERMS)
	year = models.IntegerField(default=20)
	userAccount = models.ForeignKey(UserAccount, null=True, blank=True)
	class Meta:
		unique_together = ("term", "year", "userAccount",)
	
	def termFullName(self):
		if self.term == "CC":
			return "FALL"
		elif self.term == "AA":
			return "SPRING"
		else:
			return "SUMMER"
	
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
	
	def __unicode__(self):
		return self.term + " " + str(self.year) + " (" + self.userAccount.username + ")"

class CourseGroup(models.Model):
	name = models.CharField(max_length=50)
	degreePlan = models.ForeignKey(DegreePlan, null=True, blank=True)
	columnNumber = models.IntegerField(default=0)
	class Meta:
		unique_together = ("name", "degreePlan",)
	def __unicode__(self):
		return self.name

class CourseSlot(models.Model):
	department = models.CharField(max_length=4, blank=True)
	number = models.IntegerField(default=0, blank=True)
	hours = models.IntegerField(default=3)
	isCompleted = models.BooleanField(default=False)
	isDepartmentEditable = models.BooleanField(default=False)
	isNumberEditable = models.BooleanField(default=False)
	isScheduled = models.BooleanField(default=False)
	notes = models.CharField(max_length=1000, null=True, blank=True)
	courseGroup = models.ForeignKey(CourseGroup, null=True, blank=True)
	semester = models.ForeignKey(Semester, null=True, blank=True, on_delete=models.SET_NULL)
	def __unicode__(self):
		return self.department + " " + str(self.number) + " (" + str(self.hours) + ")"
		
# python manage.py schemamigration planner --auto
# python manage.py migrate planner