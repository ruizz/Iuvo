from django.conf.urls import patterns, url
from planner import views

urlpatterns = patterns('',

	# Logs the user out if logged in.
	# ex: /
	url(r'^$', views.index, name='index'),

	# ex: /user/john.doe/dashboard/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/dashboard/$', views.dashboardView, name='dashboard'),
	
	# ex: /user/john.doe/account/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/account/$', views.userAccountView, name='userAccount'),

	# ex: /user/john.doe/toDropbox/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/toDropbox/$', views.toDropboxLink, name='toDropbox'),

	# ex: /user/john.doe/fromDropbox/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/fromDropbox/$', views.fromDropboxLink, name='fromDropbox'),
		
	# ex: /user/john.doe/degreeplan/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/degreeplan/$', views.degreePlanView, name='degreePlan'),
	
	# ex: /user/john.doe/schedule/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/schedule/$', views.scheduleView, name='schedule'),
	
	# ex: /user/john.doe/export/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/export/$', views.exportView, name='export'),
)