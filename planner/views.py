# Create your views here.

from django.http import HttpResponse
from planner.models import *

def index(request):
	return HttpResponse("Hello")

def userAccountPage(request, username):
	userAccount = UserAccount.objects.get(username=username)
	return HttpResponse("User Account Page for %s %s" % userAccount.firstName, userAccount.lastName)