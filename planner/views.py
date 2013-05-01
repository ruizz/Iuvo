from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from planner.models import *

def index(request):
	userAccounts = UserAccount.objects.all();
	context = { 'userAccounts': userAccounts}
	return render(request, 'planner/base_login.html', context)

def dashboardView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_myDashboard.html', context)
	
def userAccountView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	context = {	'userAccount': userAccount	}
	return render(request, 'planner/base_myAccount.html', context)

def degreePlanView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_myDegreePlan.html', context)
	
def scheduleView(request, username):
	userAccount = get_object_or_404(UserAccount, username=username)
	degreePlan = userAccount.degreePlan
	context = { 'userAccount': userAccount, 'degreePlan': degreePlan}
	return render(request, 'planner/base_mySchedule.html', context)