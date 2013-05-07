from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
import cStringIO as StringIO
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import Context, RequestContext, loader
from django.template.loader import render_to_string
from planner.models import *
from planner.degrees import *
from dropbox import client, rest, session
import urllib2,urllib
import json
import os
from django.core.urlresolvers import reverse
FACEBOOK_APP_ID='197588320365151'
FACEBOOK_API_SECRET='b654c9c0daad222b60bc62c5d04f4f8d'
APP_KEY = 'mi3ke3q34bovjs4'
APP_SECRET = '6utueoeh7kbdf21'
ACCESS_TYPE = 'app_folder'
global_session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
global_token = ""

def index(request):
	# Always log the user out
	logout(request)
	return render_to_response('planner/base_login.html', {}, context_instance=RequestContext(request))
		
@login_required
def dashboardView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	
	# Always make sure that user isn't snooping around, looking at another user's page.
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
	
	# Always make sure that user isn't snooping around, looking at another user's page.
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
	
	# Always make sure that user isn't snooping around, looking at another user's page.
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
	
	# Always make sure that user isn't snooping around, looking at another user's page.
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
	
	# Always make sure that user isn't snooping around, looking at another user's page.
	if loggedInUser == username:
		# prevent user from viewing course from another user
		if not courseSlot.courseGroup.degreePlan.userAccount == userAccount:
			raise Http404
		
		# If user requested to change info about a course.
		if request.POST:
			department = request.POST.get('department')
			number = request.POST.get('number')
			isCourseCompleted = request.POST.get('courseCompletedOption')
			semester = request.POST.get('semesterOption')
			
			# Check if changes exist. Javascript on the html page prevents user from
			#	inputting bogus entries. EX: putting a letter in a numeric field.
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
				else:
					term = semester[:2]
					year = semester[3:7]
					userSemester = Semester.objects.get(term=term, year=year, userAccount=userAccount)
					courseSlot.semester = userSemester
					courseSlot.isScheduled = True
			
			courseSlot.save()
			state="Changes saved!"
	else:
		raise Http404
	
	context = {'state':state, 'username':username, 'userAccount':userAccount, 'courseSlot':courseSlot, }
	return render_to_response('planner/base_editCourse.html', context, context_instance=RequestContext(request))

def addSemesterView(request, username):
	state = "Add a new semester here."
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	
	# Always make sure that user isn't snooping around, looking at another user's page.
	if loggedInUser == username:
		# If user requests to add a semester.
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

@login_required
def deleteSemesterView(request, username, semesterpk):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	semester = get_object_or_404(Semester, pk=semesterpk)
	
	# Always make sure that user isn't snooping around, looking at another user's page.
	if loggedInUser == username:
		# prevent user from viewing course from another user
		if not semester.userAccount == userAccount:
			raise Http404
		
		# Each course has a flag to tell if it is scheduled to a semester. We need to change
		# all of the courses in the semester to false before deleting the semester.
		for courseSlot in semester.courseslot_set.all():
			courseSlot.isScheduled = False
			courseSlot.save()
		
		semester.delete()
	else:
		raise Http404
	
	url = '/user/%s/schedule' % request.user.username
	return HttpResponseRedirect(url)
		
@login_required
def exportView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	state = "Nothing"
	# Always make sure that user isn't snooping around, looking at another user's page.
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		if request.POST:
			state = request.POST.get('state')
		
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters, 'state':state}
		return render(request, 'planner/base_export.html', context)
	else:
		raise Http404

@login_required
def importView(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_import.html', context)
	else:
		raise Http404

@login_required
def importAction(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		# parse json and load degreeplan into database and user account
		degreePlan = userAccount.degreeplan_set.all()[0]
		semesters = userAccount.semester_set.all()
		context = { 'userAccount': userAccount, 'degreePlan': degreePlan, 'semesters': semesters}
		return render(request, 'planner/base_import.html', context)
	else:
		raise Http404

@login_required
def exportFile(request, username):
	loggedInUser = request.user.username
	userAccount = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		degreePlan = userAccount.degreeplan_set.all()[0]
		context = {'degreePlan': degreePlan}

		# generate file
		tempfile = StringIO.StringIO()
		jstring = render_to_string('planner/degreeplan.json', context)
		tempfile.write(jstring)
		tempfile.seek(0)


		# generate response
		response = HttpResponse(tempfile, content_type='application/json')
		response['Content-Disposition'] = 'attachment; filename=degreePlan.json'
		#response['Content-Length'] = 500
		return response
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
	account = get_object_or_404(UserAccount, username=username)
	context = {'userAccount': account}
	if request.GET.get('not_approved'):
		print "user denied"
	else:
		access_token = global_session.obtain_access_token(global_token)
		account.dropboxLinked = True
		account.dropboxToken = access_token.key
		account.dropboxTokenSecret = access_token.secret
		account.save()
	return render(request, 'planner/base_myAccount.html', context)

@login_required
def uploadToDropbox(request, username):
	loggedInUser = request.user.username
	account = get_object_or_404(UserAccount, username=username)
	if loggedInUser == username:
		new_session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		new_session.set_token(account.dropboxToken,account.dropboxTokenSecret)
		newclient = client.DropboxClient(new_session)

		degreePlan = account.degreeplan_set.all()[0]
		context = {'degreePlan': degreePlan}

		# generate file
		tempfile = StringIO.StringIO()
		content = render_to_string('planner/degreeplan.json', context)
		# filename = "/{0}.json".format(degreePlan.name.replace(' ', '_'))
		filename = "/degree_plan.json"

		response = newclient.put_file(filename, content , True)
		state = "Successfully exported your degree plan to Dropbox!"
		context = {'userAccount': account, 'state':state, }
		return render(request, 'planner/base_export.html', context)
	else:
		raise Http404

@login_required
def downloadFromDropbox(request, username):
	account = get_object_or_404(UserAccount, username=username)
	new_session = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
	new_session.set_token(account.dropboxToken,account.dropboxTokenSecret)
	newclient = client.DropboxClient(new_session)
	f, metadata = newclient.get_file_and_metadata('/degree_plan.json')
	# out = open('magnum-opus.txt', 'w')#don't realy need
	jsonstring = f.read()
	#print jsonstring
	dp = json.loads(jsonstring)
	# print dp

	
	print "name: ", dp['name']
	cgs = dp['courseGroups']
	for group in cgs:
		print "  {0}({1})".format(group['name'], group['columnNumber'])
		for slot in group['courseSlots']:
			print "    {0}{1}({2})".format(slot['dept'], slot['number'], slot['isDepartmentEditable']);
	
	degreePlan = account.degreeplan_set.all()[0]
	degreePlan.delete()
	newDegreePlan = DegreePlan(name=dp['name'], userAccount=account)
	newDegreePlan.save()
	
	for group in cgs:
		newCourseGroup = CourseGroup(name=group['name'], degreePlan=newDegreePlan, columnNumber=group['columnNumber'])
		newCourseGroup.save()
		for slot in group['courseSlots']:
			newCourseSlot = CourseSlot(department=slot['dept'], number=slot['number'], hours=slot['hours'], isDepartmentEditable=slot['isDepartmentEditable'] , isNumberEditable=slot['isNumberEditable'] ,isScheduled=False, notes='', courseGroup=newCourseGroup)
			newCourseSlot.save()
			
	# out.write(f.read())#dont really need
	# out.close()#
	state = "Successfully imported your degree plan from Dropbox!"
	context = {'userAccount': account, 'state':state, }
	return render(request, 'planner/base_export.html', context)
	
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
	fql_query_url = "SELECT first_name,last_name,email,education,uid FROM user WHERE uid=me"
	fql_query_url = urllib.quote(fql_query_url)+"()"
	url = "https://graph.facebook.com/fql?q=" + fql_query_url + '&access_token='+access_token
	data = urllib.urlopen(url).read()
	pyData=json.loads(data)
	print pyData
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
	
	username = pyData["data"][0]["uid"]
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
	
