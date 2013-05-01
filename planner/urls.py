from django.conf.urls import patterns, url
from planner import views

urlpatterns = patterns('',
	# ex: /
	url(r'^$', views.index, name='index'),
	
	# ex: /user/john.doe/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/dashboard/$', views.dashboardView, name='dashboard'),
	
	# ex: /user/john.doe/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/account/$', views.userAccountView, name='userAccount'),

	# ex: /user/john.doe/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/dropbox/$', views.dropboxLink, name='dropbox'),
		
	# ex: /user/john.doe/degreeplan/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/degreeplan/$', views.degreePlanView, name='degreePlan'),
	
	# ex: /user/john.doe/schedule/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/schedule/$', views.scheduleView, name='schedule'),
)