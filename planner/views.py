from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import Context, RequestContext, loader
from planner.models import *
from planner.degrees import *
from dropbox import client, rest, session
import urllib2,urllib
import json
FACEBOOK_APP_ID='197588320365151'
FACEBOOK_API_SECRET='b654c9c0daad222b60bc62c5d04f4f8d'

def index(request):
	logout(request)
	state = "Please log in."
	username = password = ''
	if request.POST:
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				state = "Login success!"
				url = '/user/%s/dashboard' % request.user.username
				return HttpResponseRedirect(url)
			else:
				state = "Inactive account."
		else:
			state = "Incorrect username/password."
	return render_to_response('planner/base_login.html', {'state':state, 'username':username}, context_instance=RequestContext(request))

def registerView(request, returnTuple = []):
	logout(request)
	state = "Please Register."
	firstname = lastname = email = username = password = school = ''
	if returnTuple:
		#user used facebook to get data, we fill in for them
		print returnTuple
		state = "Please pick a username and password now."
		firstname = returnTuple[0]
		lastname = returnTuple[1]
		email = returnTuple[2]
		school = returnTuple[3]
	if request.POST:
		# Get all the data that user entered
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		school = request.POST.get('school')
		
		# Make sure none of it is empty
		state = "Missing: "
		if not firstname:
			state += "First "
		if not lastname:
			state += "Last "
		if not email:
			state += "Email "
		if not username:
			state += "User "
		if not password:
			state += "Pass "
		if not school:
			state += "School "
		
		# If none of it is empty
		if firstname and lastname and email and username and password and school:
			# create auth account
			try:
				new_user = User.objects.create_user(username, email, password)
			except IntegrityError:
				state = "User already exists."
				return render_to_response('planner/base_register.html', {'state':state, 'username':username}, context_instance=RequestContext(request))
			else:
				state = "Account Created!"
			
			# create planner account
			newUserAccount = UserAccount(firstName=firstname, lastName=lastname, username=username, school=school)
			newUserAccount.save()
			newUserAccountPk = newUserAccount.pk
			newDegreePlan = degreeComputerScience(newUserAccountPk)
			
			# Take the user back to the home page
			url = '/'
			return HttpResponseRedirect(url)
	# What's this? The user must have left some fields blank. It's time to lay down the law. Let them know.
	return render_to_response('planner/base_register.html', {'state':state, 'username':username, 'firstname':firstname , 'lastname':lastname, 'email':email, 'school':school }, context_instance=RequestContext(request))
#def registerView(request,extraTuple):

@login_required
def dashboardView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_myDashboard.html', context)
	else:
		raise Http404

@login_required
def userAccountView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_myAccount.html', context)
	else:
		raise Http404

@login_required
def degreePlanView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_myDegreePlan.html', context)
	else:
		raise Http404

@login_required
def scheduleView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_mySchedule.html', context)
	else:
		raise Http404

def editCourseView(request, username, coursepk):
	state = ""
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	courseSlot = get_object_or_404(CourseSlot, pk=coursepk)
	
	if loggedInUser == username:
		# prevent user from viewing course from another user
		if not courseSlot.courseGroup.degreePlan.userAccount == userAccount:
			raise Http404
		
		if request.POST:
			department = request.POST.get('department')
			number = request.POST.get('number')
			isCourseCompleted = request.POST.get('courseCompletedOption')
			semester = request.POST.get('semesterOption')
			
			print(department)
			print(number)
			print(isCourseCompleted)
			print(semester)
			
			if department:
				courseSlot.department = department
			if number:
				courseSlot.number = number
			if isCourseCompleted == "True":
				courseSlot.isCompleted = True
			if isCourseCompleted == "False":
				courseSlot.isCompleted = False
				
			if semester:
				if semester == "No Selection":
					courseSlot.semester = None
					courseSlot.isScheduled = False
				if not semester == "No Selection":
					term = semester[:2]
					year = semester[3:7]
					userSemester = Semester.objects.get(term=term, year=year, userAccount=userAccount)
					courseSlot.semester = userSemester
					courseSlot.isScheduled = True
			
			courseSlot.save()
			state="Changes saved!"
	else:
		raise Http404
		
	return render_to_response('planner/base_editCourse.html', {'state':state, 'username':username, 'userAccount':userAccount, 'courseSlot':courseSlot, }, context_instance=RequestContext(request))

def addSemesterView(request, username):
	state = "Add a new semester here."
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		if request.POST:
			term = request.POST.get('termOption')
			year = request.POST.get('yearOption')
			year = "20" + year
			
			if not len(year) == 4:
				state = "Please enter a valid year."
				return render_to_response('planner/base_addsemester.html', {'state':state, 'username':username, 'userAccount':userAccount, }, context_instance=RequestContext(request))
			
			if term == "NO":
				state = "You must select a term."
				return render_to_response('planner/base_addsemester.html', {'state':state, 'username':username, 'userAccount':userAccount, }, context_instance=RequestContext(request))

			testSemester = Semester.objects.filter(term=term, year=year, userAccount=userAccount).count()
			
			if testSemester == 0:
				createdSemester = Semester.objects.create(term=term, year=year, userAccount=userAccount)
				state="Semester added!"
			else:
				state="Semester already exists."
			
	else:
		raise Http404
		
	return render_to_response('planner/base_addsemester.html', {'state':state, 'username':username, 'userAccount':userAccount, }, context_instance=RequestContext(request))
	
def deleteSemesterView(request, username, semesterpk):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	semester = get_object_or_404(Semester, pk=semesterpk)
	if loggedInUser == username:
		# prevent user from viewing course from another user
		if not semester.userAccount == userAccount:
			raise Http404
		
		for courseSlot in semester.courseslot_set.all():
			courseSlot.isScheduled = False
			courseSlot.save()
		
		semester.delete()
	else:
		raise Http404
	
	url = '/user/%s/schedule' % request.user.username
	return HttpResponseRedirect(url)
	
@login_required
def degreePlanView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_myDegreePlan.html', context)
	else:
		raise Http404	
		
		
@login_required
def exportView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_export.html', context)
	else:
		raise Http404

@login_required
def toDropboxLink(request, username):
	# code to send user to dropbox
	url = ''#build_authorize_url( token, reverse('fromDropbox' username=username))
	return redirect(url)

@login_required
def fromDropboxLink(request, username):
	
	# token = ''
	# account = get_object_or_404(UserAccount, username=username)
	# account.dropboxLinked = True
	# account.dropboxToken = token
	# account.save()

	pass
	

def toFacebookLink(request):
	url = 'https://www.facebook.com/dialog/oauth?%20client_id=197588320365151%20&redirect_uri=http://localhost:8000/register/facebook/return&scope=email%2Cuser_education_history'
	return redirect(url)

def fromFacebookLink(request):
	url = '/register/'
	code = request.GET.get('code')
	#print(code)
	url = 'https://graph.facebook.com/oauth/access_token?client_id=197588320365151&redirect_uri=http://localhost:8000/register/facebook/return&client_secret=b654c9c0daad222b60bc62c5d04f4f8d&code=%s' % code
	response = urllib2.urlopen(url)
	html = response.read()
	lhs,access_token = html.split('access_token=')
	access_token,expire_time = access_token.split('&expires=')
	#lhs never used, holds dummy value for string split
	fql_query_url = "SELECT first_name,last_name,email,education FROM user WHERE uid=me"
	fql_query_url = urllib.quote(fql_query_url)+"()"
	url = "https://graph.facebook.com/fql?q=" + fql_query_url + '&access_token='+access_token
	data = urllib.urlopen(url).read()
	#TODO store access token, and expire_time, and time initiated to check against
	#take json data and put it in a form for the user to fill out, ask them for a username and password, 
	#and any missing information
	pyData=json.loads(data)
	education = pyData["data"][0]["education"]
	edu_var = ''
	#iterate through their education history to find their college
	for index in range(len(education)):
		print education[index]
		if education[index]['type'] == "College" :
			print "found match"
			edu_var = education[index]['school']['name']
	returnTuple = pyData["data"][0]["first_name"],pyData["data"][0]["last_name"],pyData["data"][0]["email"],edu_var
	#return back to the register view but fill in the fields
	return registerView(request, returnTuple)
	