from django.db import models
from django.db import models
	
class UserAccount(models.Model):
	#One Personal Info, Degree plan, and degree schedule implicit
	def __unicode__(self):
		return self.personlInfo.lastName + ", " + self.personlInfo.firstName

class PersonalInfo(models.Model):
	#FacebookData needs to be implimented
	#
	userAccount = models.OneToOneField(UserAccount, related_name='personlInfo')
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	school = models.CharField(max_length=200)

	def __unicode__(self):
		return self.lastName + ", " + self.firstName

class DegreePlan(models.Model):
	#Many courseGroups implicit
	userAccount = models.OneToOneField(UserAccount, related_name='degreePlan')
	name = models.CharField(max_length=200)
	major = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class CourseGroup(models.Model):
	#Many CourseChoice implicit
	degreePlan = models.ForeignKey(DegreePlan, related_name='courseGroups')
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class CourseChoice(models.Model): #dynamic course, choose these
	#Many Courses impicit, or just one
	name = models.CharField(max_length=200)
	courseGroup = models.ForeignKey(CourseGroup, related_name='courseChoices')
	courseSelected = models.BooleanField(default=False)
	selectedCourse = models.ForeignKey('Course')

	def __unicode__(self):
		if courseSelected:
			sel = selectedCourse.__unicode__()
		else :
			sel = "no selection"
		return self.name + "(" + sel + ")"
	
class DegreeSchedule(models.Model): 
	# many Semesters implicit
	userAccount = models.OneToOneField(UserAccount, related_name='degreeSchedule')

	def __unicode__(self):
		return userAccount.personlInfo.lastName

class Semester(models.Model): 
	degreeSched = models.ForeignKey(DegreeSchedule, related_name='semesters')
	term = models.CharField(max_length=200)
	year = models.IntegerField(default=2000)
	#Many Courses implicit

	def __unicode__(self):
		return self.term + " " + str(self.year)

class Course(models.Model): #static course, you have to take this
	courseChoices = models.ManyToManyField(CourseChoice, related_name='courses', blank=True)
	semesters = models.ManyToManyField(Semester, related_name='courses', blank=True)
	#hardcoded for TAMU department names and course numbers
	#below are basically static fields
	department = models.CharField(max_length=4)
	number = models.IntegerField(default=0) #specify length or max
	hours = models.IntegerField(default=0) #specify length or max
	name = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.department + " " + str(self.number) + " (" + str(self.hours) + ")" 