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
from django.core.urlresolvers import reverse
FACEBOOK_APP_ID='197588320365151'
FACEBOOK_API_SECRET='b654c9c0daad222b60bc62c5d04f4f8d'
APP_KEY = 'mi3ke3q34bovjs4'
APP_SECRET = '6utueoeh7kbdf21'
ACCESS_TYPE = 'app_folder'
global_session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
global_token = ""

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
		semesters = userAccount.semester_set.all().order_by('year')
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
			
			if department:
				courseSlot.department = department.upper()
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
	userAccount = get_object_or_404(UserAccount, username=username)
        request_token = global_session.obtain_request_token()
        global global_token
        global_token=request_token
	url = global_session.build_authorize_url(request_token, oauth_callback=request.build_absolute_uri(reverse('fromDropbox',kwargs={'username':userAccount.username})))
        return redirect(url)

@login_required
def fromDropboxLink(request, username):
	
	access_token = global_session.obtain_access_token(global_token)
	account = get_object_or_404(UserAccount, username=username)
	account.dropboxLinked = True
	account.dropboxToken = access_token
	account.save()
	context = {'userAccount': account}
	return render(request, 'planner/base_myAccount.html', context)
	
def toFacebookLink(request):
	print "To facebook link"
	url = 'https://www.facebook.com/dialog/oauth?%20client_id=197588320365151%20&redirect_uri=http://localhost:8000/register/facebook/return&scope=email%2Cuser_education_history'
	return redirect(url)

def fromFacebookLink(request):
	
	# If user denies Facebook authentication
	if request.GET.get('error') == "access_denied":
		return HttpResponseRedirect('/')
	
	code = request.GET.get('code')
	#print(code)
	url = 'https://graph.facebook.com/oauth/access_token?client_id=197588320365151&redirect_uri=http://localhost:8000/register/facebook/return&client_secret=b654c9c0daad222b60bc62c5d04f4f8d&code=%s' % code
	response = urllib2.urlopen(url)
	html = response.read()
	lhs,access_token = html.split('access_token=')
	access_token,expire_time = access_token.split('&expires=')
	#lhs never used, holds dummy value for string split
	fql_query_url = "SELECT first_name,last_name,email,education,username FROM user WHERE uid=me"
	fql_query_url = urllib.quote(fql_query_url)+"()"
	url = "https://graph.facebook.com/fql?q=" + fql_query_url + '&access_token='+access_token
	data = urllib.urlopen(url).read()
	#TODO store access token, and expire_time, and time initiated to check against
	#take json data and put it in a form for the user to fill out, ask them for a username and password, 
	#and any missing information
	pyData=json.loads(data)
	education = pyData["data"][0]["education"]
	school = ''
	#iterate through their education history to find their college
	for index in range(len(education)):
		if education[index]['type'] == "College" :
			school = education[index]['school']['name']
	# returnTuple = pyData["data"][0]["first_name"],pyData["data"][0]["last_name"],pyData["data"][0]["email"],edu_var
	firstname = pyData["data"][0]["first_name"]
	lastname = pyData["data"][0]["last_name"]
	email = pyData["data"][0]["email"]
	#return back to the register view but fill in the fields
	context = { 'firstname':firstname, 'lastname':lastname, 'email':email, 'school':school, }
	
	username = pyData["data"][0]["username"]
	# Best. Password. Ever. (Make more secure one day?)
	password = "password"

	# IF WE HAVE ALL THE INFO WE NEED.
	if firstname and lastname and email and username and password and school:
		# Attempt to create a user Auth account
		try:
			new_user = User.objects.create_user(username, email, password)
		except IntegrityError:
			# If it already exists, re-save the token (just to be safe),
			# log the user in, and redirect to the dashboard.
			plannerAccount = UserAccount.objects.get(username=username)
			plannerAccount.facebookToken = access_token
			plannerAccount.save()
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				url = '/user/%s/dashboard' % username
				return HttpResponseRedirect(url)
		
		# Auth account is created, create the account for our planner app
		newUserAccount = UserAccount(firstName=firstname, lastName=lastname, username=username, school=school, facebookLinked=True, facebookToken=access_token)
		newUserAccount.save()
		newUserAccountPk = newUserAccount.pk
		newDegreePlan = degreeComputerScience(newUserAccountPk)
		
		# Log the user into Auth, redirect to dashboard
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
		url = '/user/%s/dashboard' % username
		return HttpResponseRedirect(url)
	
	return HttpResponseRedirect('/')
	
