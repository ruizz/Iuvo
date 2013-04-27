from django.conf.urls import patterns, url
from planner import views

urlpatterns = patterns('',
	# ex: /
	url(r'^$', views.index, name='index'),
	# ex: /user/john.doe/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/account/$', 
		views.userAccountView, name='userAccount'),
	# ex: /user/john.doe/degreeplan/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/degreeplan/$', views.degreePlanView, name='degreePlan'),
)