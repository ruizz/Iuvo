from django.db import models
	
class UserAccount(models.Model):
	#One DegreePlan and DegreeSchedule implicit
	#selections
	firstName = models.CharField(max_length=200)
	lastName = models.CharField(max_length=200)
	username = models.CharField(max_length=200)
	school = models.CharField(max_length=200)
	dropboxLinked = models.BooleanField(default=False)
	dropboxToken = models.CharField(max_length=50, default="")
	degreePlan = models.ForeignKey('DegreePlan')
	# need dropbox and facebook account data

	def __unicode__(self):
		return self.lastName + ", " + self.firstName

class DegreePlan(models.Model):
	#Many courseGroups implicit
	name = models.CharField(max_length=200)
	major = models.CharField(max_length=200) # not sure what this is

	def __unicode__(self):
		return self.name

class CourseGroup(models.Model):
	#Many CourseChoices implicit
	degreePlan = models.ForeignKey(DegreePlan, related_name='courseGroups')
	name = models.CharField(max_length=200)
	colNum = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name

class CourseChoice(models.Model): #dynamic course, choose these
	#Many Courses impicit, or just one
	name = models.CharField(max_length=200, blank=True, null=True)
	courseGroup = models.ForeignKey(CourseGroup, related_name='courseChoices')
	required = models.BooleanField(default=False) 

	def __unicode__(self):
		#return str(self.courses.count())
		if self.required and self.courses.count() == 1:
			c = self.courses.all()[0]
			return str(c)
		elif self.name:
			return self.name
		else:
			return 'CourceChoice' + str(self.id)
	
class DegreeSchedule(models.Model): 
	# many Semesters implicit
	userAccount = models.OneToOneField(UserAccount, related_name='degreeSchedule')

	def __unicode__(self):
		account = self.userAccount
		return account.firstName + " " + account.lastName + "'s Schedule"

class Semester(models.Model): 
	degreeSched = models.ForeignKey(DegreeSchedule, related_name='semesters')
	TERMS = (
		('FA', 'Fall'),
		('SP', 'Spring'),
		('SU', 'Summer'),
		)
	term = models.CharField(max_length=2, choices=TERMS)
	year = models.IntegerField(default=2000)
	#selections

	def __unicode__(self):
		return self.term + " " + str(self.year)

class Course(models.Model): 
	courseChoices = models.ManyToManyField(CourseChoice, related_name='courses', blank=True)
	# semesters = models.ManyToManyField(Semester, related_name='courses', blank=True)
	# courseGroups = models.ManyToManyField(CourseGroup, related_name='courses', blank=True)
	department = models.CharField(max_length=4)
	number = models.IntegerField(default=0)
	hours = models.IntegerField(default=0) 
	name = models.CharField(max_length=200, blank=True)

	def __unicode__(self):
		return self.department + " " + str(self.number) + " (" + str(self.hours) + ")" 

class CourseSelection(models.Model):
    selectedCourse = models.ForeignKey(Course, related_name='selections', default=None, blank=True, null=True)
    userAccount = models.ForeignKey(UserAccount, related_name='selections')
    courseChoice = models.ForeignKey(CourseChoice, related_name='selections')
    semester = models.ForeignKey(Semester, related_name='selections', default=None, blank=True, null=True)

    def __unicode__(self):
        if self.selectedCourse:
        	return str(self.selectedCourse)
        else:
        	return str(self.courseChoice)
