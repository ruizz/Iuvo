from django.db import models
class Course(models.Model):
	#For making work
	pass
	
class UserAccount(models.Model):
	#One Personal Info, Degree plan, and degree schedule implicit
	pass

class PersonalInfo(models.Model):
	#FacebookData needs to be implimented
	#
	userAccount = models.OneToOneField(UserAccount)
	fistName = models.CharField(max_length = 200)
	lastName = models.CharField(max_length = 200)
	username = models.CharField(max_length = 200)
	school = models.CharField(max_length = 200)

class DegreePlan(models.Model):
	#Many courseGroups implicit
	userAccount = models.OneToOneField(UserAccount)
	name = models.CharField(max_length = 200)
	major = models.CharField(max_length = 200)

class CourseGroup(models.Model):
	#Many CourseChoice implicit
	degreePlan = models.ForeignKey(DegreePlan)
	name = models.CharField(max_length = 200)

class CourseChoice(models.Model): #dynamic course, choose these
	#Many Courses impicit, or just one
	name = models.CharField(max_length = 200)
	courseGroup = models.ForeignKey(CourseGroup)
	courseSelected = models.BooleanField(default = False)
	selectedCourse = models.ForeignKey(Course)
	
class DegreeSchedule(models.Model): 
	# many Semesters implicit
	userAccount = models.OneToOneField(UserAccount)

class Semester(models.Model): 
	degreeSched = models.ForeignKey(DegreeSchedule)
	term = models.CharField(max_length = 200)
	year = models.IntegerField(default=2000)
	#Many Courses implicit
class Course(models.Model): #static course, you have to take this
	courseChoice = models.ManyToManyField(CourseChoice)
	semester = models.ManyToManyField(Semester)
	#hardcoded for TAMU department names and course numbers
	#below are basically static fields
	department = models.CharField(max_length = 4)
	number = models.IntegerField(default=0) #specify length or max
	hours = models.IntegerField(default=0) #specify length or max
	name = models.CharField(max_length = 200)
