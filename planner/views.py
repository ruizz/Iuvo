from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import Context, RequestContext, loader
from planner.models import *

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
	return render_to_response('planner/base_login.html', {'state':state, 'username': username}, context_instance=RequestContext(request))

@login_required
def dashboardView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_myDashboard.html', context)

@login_required
def userAccountView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	context = {	'userAccount': userAccount	}
	return render(request, 'planner/base_myAccount.html', context)

@login_required
def degreePlanView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_myDegreePlan.html', context)

@login_required
def scheduleView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_mySchedule.html', context)
	
@login_required
def exportView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_export.html', context)

@login_required
def toDropboxLink(request, username):
	# code to send user to dropbox
	url = ''#build_authorize_url( token, reverse('fromDropbox' username=username))
	return redirect(url)

@login_required
def fromDropboxLink(request, username):
	

	
	pass