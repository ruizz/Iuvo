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
import urllib2

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

def registerView(request):
	logout(request)
	state = "Please Register."
	firstname = lastname = username = password = school = ''
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
	return render_to_response('planner/base_register.html', {'state':state, 'username':username}, context_instance=RequestContext(request))

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
	url = 'https://www.facebook.com/dialog/oauth?%20client_id=197588320365151%20&redirect_uri=http://localhost:8000/register/facebook/return'
	return redirect(url)

def fromFacebookLink(request):
	url = '/register/'
	code = request.GET.get('code')
	print(code)
	url = 'https://graph.facebook.com/oauth/access_token?client_id=197588320365151&redirect_uri=http://localhost:8000/register/facebook/return&client_secret=b654c9c0daad222b60bc62c5d04f4f8d&code=%s' % code
	response = urllib2.urlopen(url)
	html = response.read()
	print(html)
	
	url = '/'
	return HttpResponseRedirect(url)
	