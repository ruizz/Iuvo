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
		
	# ex: /user/john.doe/degreeplan/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/degreeplan/$', views.degreePlanView, name='degreePlan'),
	
	# ex: /user/john.doe/schedule/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/schedule/$', views.scheduleView, name='schedule'),
	
	# ex: /user/john.doe/editcourse/1/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/editcourse/(?P<coursepk>[A-Za-z0-9.-_]+)/$', views.editCourseView, name='editCourse'),
	
	# ex: /user/john.doe/schedule/delete/1/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/schedule/delete/(?P<semesterpk>[A-Za-z0-9.-_]+)/$', views.deleteSemesterView, name='deleteSemester'),
	
	# ex: /user/john.doe/schedule/add/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/schedule/add/$', views.addSemesterView, name='addSemester'),
	
	# ex: /user/john.doe/export/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/export/$', views.exportView, name='export'),
	
	# ex: /user/john.doe/toDropbox/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/toDropbox/$', views.toDropboxLink, name='toDropbox'),

	# ex: /user/john.doe/fromDropbox/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/fromDropbox/$', views.fromDropboxLink, name='fromDropbox'),

        # ex: /user/john.doe/uploadTo/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/uploadTo/$', views.uploadToDropbox, name='uploadTo'),

        # ex: /user/john.doe/downloadFrom/
	url(r'^user/(?P<username>[A-Za-z0-9.-_]+)/downloadFrom/$', views.downloadFromDropbox, name='downloadFrom'),
	
	# ex: /facebook/
	url(r'^facebook/$', views.toFacebookLink, name='facebook'),
	
	# ex: /facebook/return/
	url(r'^register/facebook/return$', views.fromFacebookLink, name='facebookReturn'),

)
