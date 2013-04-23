# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from planner.models import *

def index(request):
	userAccounts = UserAccount.objects.all();
	context = { 'userAccounts': userAccounts}
	return render(request, 'planner/index.html', context)

def userAccountView(request, username):

	userAccount = get_object_or_404(UserAccount, username=username)
	context = {	'userAccount': userAccount	}
	
	return render(request, 'planner/userAccount.html', context)

def degreePlanView(request, dpID):
	degreePlan = get_object_or_404(DegreePlan, id=dpID)
	context = { 'degreePlan': degreePlan}
	return render(request, 'planner/degreePlan.html', context)